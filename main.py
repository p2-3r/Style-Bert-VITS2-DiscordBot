import sys
import re

from style_bert_vits2.nlp import bert_models  # type: ignore
from style_bert_vits2.constants import Languages  # type: ignore

from src import global_data  # type: ignore
from src.bots import bot
from src.json_utils.botdata import BotJson
from src.sbv2.models import get_modelfolder_names
from src.tools.colorprint import Existing as clp

if __name__ == "__main__":
    # モデルが model_assets フォルダにあるかチェック
    folder_names = get_modelfolder_names()
    if len(folder_names) == 0:
        clp.error("モデルがありません。model_assetsフォルダーにモデルを入れてから再起動してください。")
        input()
        sys.exit()

    bot_json = BotJson()
    bot_token = bot_json.data["bot_token"]

    # トークンの形式じゃなければユーザーにトークンを入力してもらう
    if not re.match(".+\..+\..+", bot_token):  # type: ignore
        print("-"*50)
        print("初期設定を行います。Botのトークンを入力してください。")
        print("-"*50)

        while True:
            input_token = input("TOKEN: ")

            input_token = input_token.replace("\"", "")
            if re.match(".+\..+\..+", input_token):  # type: ignore
                bot_json.data["bot_token"] = input_token
                bot_json.write(bot_json.data)
                break

            else:
                print("トークンの形式ではありません。\nもう一度入力してください。")
                continue

    # SBV2のモデル読み込み
    bert_models.load_model(Languages.JP, "ku-nlp/deberta-v2-large-japanese-char-wwm")
    bert_models.load_tokenizer(Languages.JP, "ku-nlp/deberta-v2-large-japanese-char-wwm")

    # Botを実行
    bot.run()
