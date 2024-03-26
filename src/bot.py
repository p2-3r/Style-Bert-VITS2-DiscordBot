from typing import Union
from pathlib import Path

import discord

from src import data
from src.data import botdata

PREFIX = botdata.prefix
DEVICE = botdata.read_all()["device"]
READ_LIMIT = botdata.read_all()["read_limit"]

fp = Path("./downloads/ffmpeg-master-latest-win64-gpl/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe")
if fp.exists():
    ffmpeg_path = str(fp.absolute())
else:
    ffmpeg_path = "ffmpeg"

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

# joinコマンドが打たれたギルドとチャンネルのペアを登録しておく用の変数
read_channel: dict[str, int] = {}

# エラーを起こさないために待機して再生するための変数
play_waitdict: dict[str, list[Union[discord.Message, discord.Interaction]]] = {}


if True:  # 反応するためのコマンドを読み込み
    from src.commands import on_ready, on_message, on_voice_state_update, on_interaction, slash

client.run(botdata.token)
