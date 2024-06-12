from typing import Union

import discord

from src.json_utils.userdata import UserJson


def run(ctx: Union[discord.Message, discord.Interaction]) -> discord.Embed:

    if isinstance(ctx, discord.Message):
        user = UserJson(ctx.author.id)
        user_name = ctx.author.name
    elif isinstance(ctx, discord.Interaction):
        user = UserJson(ctx.user.id)
        user_name = ctx.user.name
    else:
        raise AssertionError("guild is None")

    description = f"**モデル**: {user.data['model_name']}\n" \
                  f"**話者**: {user.data['speaker_name']}\n" \
                  f"**スタイル**: {user.data['style']}"

    embed = discord.Embed(title=f"**{user_name}** の現在のモデル情報", description=description)

    return embed
