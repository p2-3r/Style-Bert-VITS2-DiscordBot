import discord

from src.bot import client
from src.data import botdata
from src.bot import PREFIX, READ_LIMIT, play_waitdict, read_channel

# ボイスチャンネルに誰かが参加したときなどの処理


@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):

    # 自分自身の変化の場合反応しない
    if member.id == client.user.id:
        return

    elif before.channel is not None:

        # ボイスチャンネルがBOTだけになったら自動的に抜ける処理
        check_list = [len(before.channel.members) != 1,  # 人数が一人だけではないなら反応しない
                      before.channel.members[0] != client.user]  # それが自分ではないなら反応しない

        if not any(check_list):
            play_waitdict[f"{before.channel.guild.id}"] = []  # そのサーバーのwaitlistを初期化
            await before.channel.guild.voice_client.disconnect()

            if f"{before.channel.guild.id}" in read_channel:
                channel_id = read_channel.pop(f"{before.channel.guild.id}")
                channel = client.get_channel(channel_id)
                await channel.send("ボイスチャンネルがBOTのみになったので自動退出しました")
