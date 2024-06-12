from typing import Union

import discord

from src.global_data import read_channel, play_waitdict


async def run(ctx: Union[discord.Message, discord.Interaction]) -> str:
    if ctx.guild is not None:
        guild = ctx.guild
    else:
        raise AssertionError("guild is None")

    if guild.voice_client is None:
        return "接続していません"

    else:
        read_channel.pop(f"{guild.id}")
        play_waitdict[f"{guild.id}"] = []

        ctx.guild.voice_client.stop()  # type: ignore
        await guild.voice_client.disconnect()  # type: ignore
        return "退出しました"
