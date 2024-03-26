import re
import sys

from src import data
from src.data import botdata
from src.model import get_modelfolders
from src.ColorPrint import Existing as clp

json_ = botdata.read_all()

folders = get_modelfolders()
if folders == []:
    clp.error("モデルがありません。model_assetsフォルダーにモデルを入れてから再起動してください。")
    input()
    sys.exit()


if not re.match(".+\..+\..+", json_["bot_token"]):
    print("-"*50)
    print("初期設定を行います。Botのトークンを入力してください。")
    print("-"*50)

    while True:
        input_token = input("TOKEN: ")

        input_token = input_token.replace("\"", "")
        try:
            botdata.token = input_token
        except ValueError:
            print("トークンの形式ではありません。\nもう一度入力してください。")
            continue

        break

if True:
    from src import bot  # Botを実行
