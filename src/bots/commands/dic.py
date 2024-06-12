from typing import Union

import discord

from src.json_utils.serverdata import ServerJson


class DicView(discord.ui.View):
    def __init__(self, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)

        self.add_item(discord.ui.Button(label="add", style=discord.ButtonStyle.primary, custom_id="dict_add"))
        self.add_item(discord.ui.Button(label="remove", style=discord.ButtonStyle.secondary, custom_id="dict_remove"))


def run(ctx: Union[discord.Message, discord.Interaction]) -> tuple[discord.Embed, discord.ui.View]:
    if ctx.guild is not None:
        guild = ctx.guild
    else:
        raise AssertionError("guild is None")

    server = ServerJson(guild.id)
    server_dict: dict[str, str] = server.data["dic"]

    embed = discord.Embed(title="このサーバーの辞書")

    if server_dict != {}:
        description = ""
        for i, [before, after] in enumerate(server_dict.items()):
            if i == 0:
                description = description + f"{before} -> {after}"
            else:
                description = description + f"\n{before} -> {after}"

            if len(description) <= 4095:
                embed = discord.Embed(title="このサーバーの辞書", description=description)
            else:
                embed = discord.Embed(title="登録されている単語が多すぎたため表示できませんでした。")
    else:
        embed = discord.Embed(title="このサーバーではまだ何も登録されていません。")

    view = DicView()

    return embed, view
