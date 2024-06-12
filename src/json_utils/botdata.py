from pathlib import Path
from typing import TypedDict

from src.json_utils.read_write import JsonFile


# 読み込んだデータの型ヒント
class BotJsonType(TypedDict):
    bot_token: str
    device: str
    read_limit: int
    default_model: str
    prefix: str
    models_upperlimit: int


# Botの設定ファイル読み込み用クラス
class BotJson():
    path: Path
    data: BotJsonType

    json_template: BotJsonType = {
        "bot_token": "",
        "device": "cuda",
        "read_limit": 50,
        "default_model": "",
        "prefix": "s!",
        "models_upperlimit": 3
    }

    def __init__(self, *, path: Path = Path("./data.json")) -> None:
        self.json = JsonFile(path)
        self.path = path

        # もしbotのJsonファイルがなければ作成
        if not self.path.exists():
            self.json.write(self.json_template)

        # 読み込んだjsonにないキーがあれば追加する
        data_dict = self.read()
        data_keys = data_dict.keys()

        flag = False
        for i in self.json_template.keys():
            if i not in data_keys:
                data_dict[i] = self.json_template[i]
                flag = True

        if flag:
            self.json.write(data_dict)

        # self.data に data.json の情報を入れておく
        self.data = self.read()

    # jsonファイルに読み書きするメソッド

    def read(self) -> BotJsonType:
        get_json = self.json.read()
        return BotJsonType(get_json)

    def write(self, data: BotJsonType) -> None:
        self.json.write(data)

    async def async_read(self) -> BotJsonType:
        get_json = await self.async_read()
        return BotJsonType(get_json)

    async def async_write(self, data: BotJsonType) -> None:
        await self.async_write(data)
