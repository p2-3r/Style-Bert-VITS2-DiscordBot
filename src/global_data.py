from pathlib import Path
from typing import Union
import discord

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

# joinコマンドが打たれたギルドとチャンネルのペアを登録しておく用の変数
read_channel: dict[str, int] = {}

# エラーを起こさないために待機して再生するための変数
play_waitdict: dict[str, list[Union[discord.Message, discord.Interaction]]] = {}


# ffmpegが下のパスにあるならそれを使う、ないならpcの環境変数のffmpegを使う
fp = Path("./downloads/ffmpeg-master-latest-win64-gpl/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe")
if fp.exists():
    ffmpeg_path = str(fp.absolute())
else:
    ffmpeg_path = "ffmpeg"
