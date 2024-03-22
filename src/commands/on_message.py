import wave
import asyncio
import io
from pathlib import Path

import discord
from scipy.io import wavfile as sciwav

from src.commands import action
from src.bot import client, read_channel, play_waitdict, PREFIX, READ_LIMIT
from src.data import botdata
from src.infer import user_infer

# 通常のメッセージに関する処理


@client.event
async def on_message(message: discord.Message):

    # もしメッセージの送信者がBOTなら返答しない
    if message.author.bot:
        return

    # プレフィックスから始まるメッセージへの反応
    if message.content.startswith(PREFIX):
        message_nopref = message.content[len(PREFIX):]

        if message_nopref == "":
            return  # もしプレフィックスだけなら反応しない

        elif message_nopref.startswith("ping"):
            reply = action.ping()
            await message.channel.send(reply)

        elif message_nopref.startswith("help"):
            embed = action.help()
            await message.channel.send(embed=embed)

        elif message_nopref.startswith("join"):
            reply = await action.join(message)
            await message.channel.send(reply)

        elif message_nopref.startswith("leave"):
            reply = await action.leave(message)
            await message.channel.send(reply)

        elif message_nopref.startswith("wav"):
            if message_nopref == "wav":
                await message.channel.send(f"**{PREFIX}wav** の後に生成したい音声を指定してください。")
            else:
                reply, bytes_ = await action.wav(message_nopref[4:], message)
                await message.channel.send(content=reply, file=discord.File(bytes_, filename="Message.wav"))

        elif message_nopref.startswith("model"):
            embed, view = action.display_change_model()
            await message.channel.send(embed=embed, view=view)

        elif message_nopref.startswith("speaker"):
            embed, view = action.display_change_speaker(message.author)
            await message.channel.send(embed=embed, view=view)

    # BOTがそのギルドでVCに参加していた時に読み上げる
    elif message.guild.voice_client is not None:

        # セミコロンから始まっていた場合、読み上げる内容がない場合読み上げない
        if message.content.startswith(";") or message.content == "":
            return

        # joinコマンドが打たれたチャンネルかどうかをチェックする
        if message.channel.id == read_channel[f"{message.guild.id}"]:

            play_waitlist = play_waitdict[f"{message.guild.id}"]
            play_waitlist.append(message)

            # 再生中に再生しようとしてエラーを起こさないため順番に再生する
            if len(play_waitlist) == 1:
                while play_waitlist:

                    # TODO 辞書や絵文字を置換するのを追加する

                    text = play_waitlist[0].content
                    # 長すぎる場合以下略する
                    if len(text) >= READ_LIMIT + 5:
                        text = text[:READ_LIMIT] + "\n、以下略"

                    bytes_ = await user_infer(text, play_waitlist[0])

                    samplerate, data = sciwav.read(bytes_)

                    try:
                        message.guild.voice_client.play(discord.FFmpegPCMAudio(bytes_, pipe=True))

                    except AttributeError:  # 再生待機リストに残っているときにvcから抜けたときにエラーにならないように
                        pass

                    await asyncio.sleep((len(data)/samplerate) + 0.1)

                    play_waitlist.pop(0)
