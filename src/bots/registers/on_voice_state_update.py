import asyncio
from typing import Optional
import discord

from src.bots.play_sound import play_sound_on_vc
from src.json_utils.serverdata import ServerJson
from src.global_data import play_waitdict, read_channel

"""
BOTだけになった時の自動退出や、自動参加機能のプログラム
"""

def register(client: discord.Client):
    @client.event
    async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):  # type: ignore

        # 自分自身の変化の場合反応しない
        if member.id == client.user.id:  # type: ignore
            return

        elif before.channel is not None:
            # ボイスチャンネルがBOTだけになったら自動的に抜ける処理

            # 人数が一人でそれが自分なら
            if (len(before.channel.members) == 1 and before.channel.members[0] == client.user):

                play_waitdict[f"{before.channel.guild.id}"] = []  # そのサーバーのwaitlistを初期化
                await before.channel.guild.voice_client.disconnect()  # type: ignore

                if f"{before.channel.guild.id}" in read_channel:
                    channel_id = read_channel.pop(f"{before.channel.guild.id}")
                    channel = client.get_channel(channel_id)
                    await channel.send("ボイスチャンネルがBOTのみになったので自動退出しました")  # type: ignore

        elif after.channel is not None:
            # 自動参加がONになっているときに誰かがボイスチャンネルに入ると自動で入る処理
            server = ServerJson(after.channel.guild.id)
            autojoin_ch: Optional[int] = server.data["auto_join"]

            # 自分自身がそのサーバーでまだVCに参加していない、そのサーバーで自動参加がONになっている
            if (after.channel.guild.voice_client is None and isinstance(autojoin_ch, int)):

                if [f"{after.channel.guild.id}"] in read_channel.values():  # エラー回避のための待機中なら動作しない
                    return

                text_channel = client.get_channel(autojoin_ch)

                # 初期値設定
                read_channel[f"{after.channel.guild.id}"] = text_channel.id  # type: ignore
                play_waitdict[f"{after.channel.guild.id}"] = []

                await asyncio.sleep(1)  # すぐにボイスチャンネルに参加するとエラーがでるバグがあるらしい

                try:
                    await after.channel.connect()
                except Exception:
                    return

                connect_message = await text_channel.send(f"接続しました\n読み上げるチャンネル: <#{str(text_channel.id)}>")  # type: ignore

                connect_message.content = "接続しました"
                connect_message.author = member
                await play_sound_on_vc(connect_message)  # type: ignore
