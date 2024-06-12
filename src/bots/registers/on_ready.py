import discord

from src.tools.colorprint import Existing as clp
from src.json_utils.botdata import BotJson

bot_json = BotJson()
PREFIX = bot_json.data['prefix']


def register(client: discord.Client, tree: discord.app_commands.CommandTree):

    @client.event
    async def on_ready():  # type: ignore
        await client.change_presence(activity=discord.Game(name=f"{PREFIX}helpでhelpを表示"))
        clp.complete("Bot launch completed.")

        clp.info("Sync SlashCommand...")
        await tree.sync()
        clp.complete("Sync completed.")
