from typing import Any
import discord

from src.json_utils.serverdata import ServerJson


async def run(ctx: discord.Interaction) -> None:
    if ctx.guild_id is None:
        raise AssertionError("guild_id is None")

    server = ServerJson(ctx.guild_id)

    class Add_Modal(discord.ui.Modal, title="単語と読み方の登録"):
        word: discord.ui.TextInput[Any] = discord.ui.TextInput(label="単語", max_length=15)
        read: discord.ui.TextInput[Any] = discord.ui.TextInput(label="読み方", max_length=15)

        async def on_submit(self, ctx: discord.Interaction):
            await ctx.response.send_message(f"読み方を設定しました\n単語: **{self.word}** 読み方: **{self.read}**")
            await server.write_dic(f"{self.word}", f"{self.read}")

    await ctx.response.send_modal(Add_Modal())
