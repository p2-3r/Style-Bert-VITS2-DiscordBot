from pathlib import Path
import json
import re
import typing
from typing import Union, Optional
import copy

from src import model
from src.model import ModelFolder


class Json_():
    def __init__(self, path: Path) -> None:
        self.path = path

    def read_all(self) -> dict[str, typing.Any]:
        with self.path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def write_all(self, data: dict[str, typing.Any]) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)


class BotData(Json_):
    def __init__(self, path: Path) -> None:
        super().__init__(path)

    @property
    def token(self) -> str:
        data = self.read_all()
        return data["bot_token"]

    @token.setter
    def token(self, value: str):
        if not re.match(".+\..+\..+", value):
            raise ValueError("It is not in the form of a token.")

        data = self.read_all()
        data["bot_token"] = value
        self.write_all(data)

    @property
    def prefix(self):
        data = self.read_all()
        return data["prefix"]

    @prefix.setter
    def prefix(self, value: str):
        data = self.read_all()
        data["prefix"] = value
        self.write_all(data)

    @property
    def users_data(self):
        data = self.read_all()
        return data["user_data"]

    @prefix.setter
    def users_data(self, value: dict[str, typing.Any]):
        data = self.read_all()
        data["user_data"] = value
        self.write_all(data)


if True:  # 読み込まれたときの処理
    botdata = BotData(Path("./data.json"))

    data_template = {
        "bot_token": "",
        "device": "cuda",
        "read_limit": 50,
        "default_model": "",
        "prefix": "s!",
        "models_upperlimit": 3,
        "number_of_cache_models": 2,
        "user_data": {},
        "server_data": {}
    }

    # もしセーブデータがなければ作成
    if not botdata.path.exists():
        botdata.write_all(data_template)

    # data_templateに新しいキーが追加されていれば追加する
    botdata_dict = botdata.read_all()
    botdata_keys = botdata_dict.keys()

    for i in data_template.keys():
        if not i in botdata_keys:
            botdata_dict[i] = data_template[i]
        botdata.write_all(botdata_dict)


class User():
    """
    Attributes
    -
    username: (任意) 設定しておくとusernameを確認できる
    user_id: jsonからデータを取り出したいdiscordのuser_id
    speaker: 入力したuser_idの話者
    style: 入力したuser_idのstyle
    safetensor: 入力したuseridのsafetensor
    json: 入力したuser_idのjson
    npy: 入力したuser_idのnpy
    length: 入力したuser_idのlength
    """
    userdict_template = {"model_name": "None",
                         "speaker_name": "None",
                         "style": "None",
                         "length": 1.0}

    def __init__(self, user_id: int, username: Optional[str] = "Default") -> None:
        self.username = username
        self.user_id = user_id

        users_data: dict[str, typing.Any] = botdata.read_all()["user_data"]

        # ユーザーがuser_dataに存在するならそのモデル、ないならdefaultのモデル
        if f"{user_id}" in users_data.keys():
            self.userdata: dict[str, typing.Any] = users_data[f"{user_id}"]
            self.keycheck()

            users_data: dict[str, typing.Any] = botdata.read_all()["user_data"]
            self.userdata: dict[str, typing.Any] = users_data[f"{user_id}"]

            self.__temp_modelname: str = self.userdata["model_name"]
            self.is_user_indict = True
        else:
            self.userdata = copy.deepcopy(self.userdict_template)
            self.__temp_modelname = botdata.read_all()["default_model"]
            self.is_user_indict = False

        # もしそのモデル名が存在しないならモデルフォルダの一番上を選択する
        try:
            modelfolder = ModelFolder(self.__temp_modelname)
        except KeyError:
            folders = model.get_modelfolders()
            modelfolder = ModelFolder(folders[0])

        # もしその話者が存在しないなら一番最初を選択
        if self.userdata["speaker_name"] in modelfolder.speakers:
            self.speaker: typing.Any = self.userdata["speaker_name"]
        else:
            self.speaker = modelfolder.speakers[0]
            if self.is_user_indict:
                self.write_userdata("speaker_name", self.speaker)

        # もしそのスタイル名が存在しないならニュートラルまたは一番最初を選択
        if self.userdata["style"] in modelfolder.styles:
            self.style = self.userdata["style"]
        else:
            if "Neutral" in modelfolder.styles:
                self.style = "Neutral"
            else:
                self.style: typing.Any = modelfolder.styles[0]
            if self.is_user_indict:
                self.write_userdata("style", self.style)

        # ユーザーのモデル情報設定
        self.safetensor = modelfolder.latest_safetensors
        self.json = modelfolder.json
        self.npy = modelfolder.npy
        self.length: typing.Any = self.userdata["length"]

    # Templateを確認してkeyが足りなかったら足す関数
    def keycheck(self) -> None:
        for i in self.userdict_template.keys():
            if not i in self.userdata.keys():
                self.write_userdata(i, self.userdict_template[i])

    def write_userdata(self, key: str, value: Union[str, int, float]) -> None:
        if not key in self.userdict_template:
            raise KeyError("This key does not exist in the template.")

        data = botdata.read_all()
        data["user_data"][f"{self.user_id}"][key] = value
        botdata.write_all(data)


if __name__ == "__main__":
    # 使用例
    user1 = User(123456789, "Apple")
    print(user1.user_id, user1.username)
    print(user1.safetensor, user1.speaker, user1.npy, user1.json, user1.style, sep="\n")
