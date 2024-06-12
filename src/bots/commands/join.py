from typing import Optional, Union

import discord

from src.global_data import read_channel, play_waitdict


async def run(ctx: Union[discord.Message, discord.Interaction]) -> Optional[str]:
    if ctx.guild is None:
        raise AssertionError("guild is None")

    if isinstance(ctx, discord.Message):
        author = ctx.author
        guild = ctx.guild
        channel = ctx.channel
    elif isinstance(ctx, discord.Interaction):
        author = ctx.user
        guild = ctx.guild
        channel = ctx.channel
    else:
        raise AssertionError("guild is None")

    if author.voice is None:  # type: ignore
        return "ボイスチャンネルに接続してから使用してください"

    elif guild.voice_client is not None:
        return "すでにボイスチャンネルに接続しています"

    elif guild.voice_client is None:
        # 初期値設定
        read_channel[f"{guild.id}"] = channel.id  # type: ignore
        play_waitdict[f"{guild.id}"] = []

        await author.voice.channel.connect()  # type: ignore
        return f"接続しました\n読み上げるチャンネル: <#{str(channel.id)}>"  # type: ignore
