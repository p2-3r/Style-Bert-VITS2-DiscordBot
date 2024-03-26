import discord

from src.bot import client, tree, PREFIX
from src.ColorPrint import Existing as clp


# botにログインされた時の処理

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"{PREFIX}helpでhelpを表示"))
    clp.complete("Bot launch completed.")

    clp.info("Sync SlashCommand...")
    await tree.sync()
    clp.complete("Sync completed.")
