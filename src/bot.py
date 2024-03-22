import discord

from src import data
from src.data import botdata

PREFIX = botdata.prefix
DEVICE = botdata.read_all()["device"]
READ_LIMIT = botdata.read_all()["read_limit"]

intents = discord.Intents.all()
client = discord.Client(intents=intents)


# joinコマンドが打たれたギルドとチャンネルのペアを登録しておく用の変数
read_channel: dict[str, int] = {}

# エラーを起こさないために待機して再生するための変数
play_waitdict: dict[str, list[discord.Message]] = {}


if True:  # 反応するためのコマンドを読み込み
    from src.commands import on_slash, on_message, on_voice_state_update, on_interaction

client.run(botdata.token)
