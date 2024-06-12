import discord

from src.json_utils.botdata import BotJson

# data.json から設定を取得
bot_json = BotJson()
PREFIX = bot_json.data["prefix"]


def run() -> discord.Embed:
    field_dict = {f"**{PREFIX}ping**": "pong!",
                  f"**{PREFIX}wav (content)**": "指定した内容を生成してその音声ファイルを添付したメッセージを送信します",
                  f"**{PREFIX}join**": "使用した人がいるボイスチャンネルに接続します",
                  f"**{PREFIX}leave**": "ボイスチャンネルから切断します",
                  f"**{PREFIX}now**": "現在のモデル、話者、スタイルを表示します",
                  f"**{PREFIX}model**": "使用できるモデルの変更メニューを表示します",
                  f"**{PREFIX}speaker**": "現在のモデルの話者変更メニューを表示します",
                  f"**{PREFIX}style**": "現在のモデルのスタイル変更メニューを表示します。",
                  f"**{PREFIX}dic**": "サーバー辞書メニューを表示します",
                  f"**{PREFIX}server**": "自動参加などサーバーに関する設定を表示します",
                  f"**{PREFIX}about**": "このBOTについて表示します"}

    embed = discord.Embed(title="このBOTのヘルプ")

    for i, l in field_dict.items():
        embed.add_field(name=i, value=l)

    return embed
