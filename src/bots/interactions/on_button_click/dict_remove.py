from typing import Any
import discord

from src.json_utils.serverdata import ServerJson


async def run(ctx: discord.Interaction) -> None:
    if ctx.guild_id is None:
        raise AssertionError("guild_id is None")

    server = ServerJson(ctx.guild_id)

    class Remove_Modal(discord.ui.Modal, title="辞書の削除"):
        word: discord.ui.TextInput[Any] = discord.ui.TextInput(label="削除したい単語", max_length=20)

        async def on_submit(self, ctx: discord.Interaction):
            try:
                await server.delete_dic(f"{self.word}")
            except KeyError:
                await ctx.response.send_message(f"辞書に 単語: **{self.word}** は存在しません", ephemeral=True)
                return

            await ctx.response.send_message(f"辞書から読み方を削除しました\n削除した単語: **{self.word}**")

    await ctx.response.send_modal(Remove_Modal())
