from typing import Union

import discord

from src.json_utils.serverdata import ServerJson


def run(ctx: Union[discord.Message, discord.Interaction]) -> tuple[discord.Embed, discord.ui.View]:
    if ctx.guild is None:
        raise AssertionError("guild is None")

    if isinstance(ctx, discord.Message):
        guild = ctx.guild
        user = ctx.author
    elif isinstance(ctx, discord.Interaction):
        guild = ctx.guild
        user = ctx.user
    else:
        raise AssertionError("NoneError")

    server = ServerJson(guild.id)
    settings = {k: v for k, v in server.data.items() if "dic" != k}

    embed = discord.Embed(title=f"{guild.name} の現在設定")

    # embedに要素を追加(keyによっては動作を変える)
    for k, v in settings.items():
        if k == "auto_join" and v is not None:
            embed.add_field(name=f"{k}", value=f"<#{v}>")
        else:
            embed.add_field(name=f"{k}", value=f"{v}")

    view = discord.ui.View()
    if user.guild_permissions.administrator:  # もし管理者なら変更用のviewを追加する # type: ignore
        select_item = [discord.SelectOption(label=i, value=i) for i in settings.keys()]
        view.add_item(discord.ui.Select(options=select_item, custom_id="change_server_settings", placeholder="変更したい設定を選択してください..."))

    return embed, view
