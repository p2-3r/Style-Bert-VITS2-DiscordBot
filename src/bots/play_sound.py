import asyncio
from typing import Union

import discord

from src.sbv2.infer import infer_from_ctx
from src.json_utils.botdata import BotJson
from src.global_data import play_waitdict, ffmpeg_path

bot_json = BotJson()
READ_LIMIT = bot_json.data["read_limit"]


async def play_sound_on_vc(ctx: Union[discord.Message, discord.Interaction], replace: bool = False):
    """
    ctx (メッセージまたはスラッシュコマンドの入力) に基づいて音声を生成する。

    ctx の送信者のモデル設定をjsonから取り出してその設定を使用する。

    replace 引数を True にすると、ctx のサーバーの辞書で置換されたものが再生される。
    """

    play_waitlist = play_waitdict[f"{ctx.guild.id}"]  # type: ignore
    play_waitlist.append(ctx)

    # 再生中に再生しようとしてエラーを起こさないため順番に再生する
    if len(play_waitlist) == 1:
        while play_waitlist:

            if isinstance(ctx, discord.Message):
                text = str(play_waitlist[0].content)  # type: ignore
                # 長すぎる場合以下略する
                if len(text) >= READ_LIMIT + 5:
                    text = text[:READ_LIMIT] + "\n以下略"

                bytes_, sr, audio = await infer_from_ctx(text, play_waitlist[0], replace=replace)

            elif isinstance(ctx, discord.Interaction):
                if ctx.command.name == "join":  # join コマンドを使用した場合、接続しました。を再生する  # type: ignore
                    bytes_, sr, audio = await infer_from_ctx("接続しました。", play_waitlist[0], replace=replace)
                else:
                    raise AssertionError(f"Unspecified command. '{ctx.command.name}'")  # type: ignore

            else:
                raise AssertionError("Discord.Message or discord.Interaction can be specified for the argument ctx.")

            try:
                ctx.guild.voice_client.play(discord.FFmpegPCMAudio(bytes_, pipe=True, executable=ffmpeg_path))  # type: ignore

            except AttributeError:  # 再生待機リストに残っているときにvcから抜けたときにエラーにならないように
                pass

            await asyncio.sleep((len(audio)/sr) + 0.1)

            play_waitlist.pop(0)
