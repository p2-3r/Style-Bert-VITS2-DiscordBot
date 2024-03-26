from pathlib import Path
import json
import re
import typing
from typing import Optional
import copy

from networkx import is_semieulerian

from src import model
from src.model import ModelFolder


class Json_:
    def __init__(self, path: Path) -> None:
        self.path = path

    def read_all(self) -> dict[str, typing.Any]:
        with self.path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def write_all(self, data: dict[str, typing.Any]) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


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
        "user_data": {},
        "server_data": {},
    }

    # もしセーブデータがなければ作成
    if not botdata.path.exists():
        botdata.write_all(data_template)

    # data_templateに新しいキーが追加されていれば追加する
    botdata_dict = botdata.read_all()
    botdata_keys = botdata_dict.keys()

    for i in data_template.keys():
        if i not in botdata_keys:
            botdata_dict[i] = data_template[i]
        botdata.write_all(botdata_dict)


class User:
    """
    Attributes
    -
    username: (任意) 設定しておくとusernameを確認できる
    user_id: jsonからデータを取り出したいdiscordのuser_id
    model_name: モデル(フォルダ)の名前
    speaker: 入力したuser_idの話者
    style: 入力したuser_idのstyle
    safetensor: 入力したuseridのsafetensor
    json: 入力したuser_idのjson
    npy: 入力したuser_idのnpy
    length: 入力したuser_idのlength
    """

    userdict_template = {
        "model_name": "None",
        "speaker_name": "None",
        "style": "None",
        "length": 1.0,
    }

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

            self.model_name: str = self.userdata["model_name"]
            self.is_user_indict = True
        else:
            self.userdata = copy.deepcopy(self.userdict_template)
            self.model_name = botdata.read_all()["default_model"]
            self.is_user_indict = False

        # もしそのモデル名が存在しないならモデルフォルダの一番上を選択する
        try:
            modelfolder = ModelFolder(self.model_name)
        except KeyError:
            folders: list[str] = model.get_modelfolders()
            modelfolder = ModelFolder(folders[0])
            if self.is_user_indict:
                self.write_userdata("model_name", folders[0])

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
        self.length: float = self.userdata["length"]

    # Templateを確認してkeyが足りなかったら足す関数
    def keycheck(self) -> None:
        for i in self.userdict_template.keys():
            if i not in self.userdata.keys():
                self.write_userdata(i, self.userdict_template[i])

    def write_userdata(self, key: str, value: typing.Any) -> None:
        if key not in self.userdict_template:
            raise KeyError("This key does not exist in the template.")

        data = botdata.read_all()

        if f"{self.user_id}" not in data["user_data"]:
            self.create_userdata()
            data = botdata.read_all()

        data["user_data"][f"{self.user_id}"][key] = value
        botdata.write_all(data)
        data = botdata.read_all()

    def create_userdata(self):
        data = botdata.read_all()
        data["user_data"][f"{self.user_id}"] = copy.deepcopy(self.userdict_template)

        botdata.write_all(data)


class Server:
    server_template = {"dic": {},
                       "dic_onlyadmin": True,
                       "auto_join": None}

    def __init__(self, server_id: int, server_name: Optional[str] = "Default") -> None:
        self.id = server_id
        self.name = server_name

        botdata_dict = botdata.read_all()
        servers_data: dict[str, typing.Any] = botdata_dict["server_data"]

        # もしサーバーデータが作成されていなければ作成する
        if f"{self.id}" not in servers_data:
            servers_data[f"{self.id}"] = copy.deepcopy(self.server_template)
            botdata.write_all(botdata_dict)

        self.data: dict[str, typing.Any] = servers_data[f"{self.id}"]
        self.keycheck()

    # keyとvalueを指定して変更する関数
    def write_serverdata(self, key: str, value: typing.Any):
        if key not in self.server_template:
            raise KeyError("This key does not exist in the template.")

        data = botdata.read_all()
        data["server_data"][f"{self.id}"][key] = value
        botdata.write_all(data)

        self.data: dict[str, typing.Any] = botdata.read_all()["server_data"][f"{self.id}"]

    # 変換前と変換後を指定してサーバー辞書に書き込む関数
    def write_dic(self, before: str, after: str):
        data = botdata.read_all()
        data["server_data"][f"{self.id}"]["dic"][before] = after
        botdata.write_all(data)

        self.data: dict[str, typing.Any] = botdata.read_all()["server_data"][f"{self.id}"]

    def delete_dic(self, key: str):
        data = botdata.read_all()
        server_dict: dict[str, str] = data["server_data"][f"{self.id}"]["dic"]

        try:
            server_dict.pop(key)
        except KeyError:
            raise KeyError("The key does not exist in the server dictionary.")

        botdata.write_all(data)

    # Templateを確認してkeyが足りなかったら足す関数
    def keycheck(self) -> None:
        for i in self.server_template.keys():
            if i not in self.data.keys():
                self.write_serverdata(i, self.server_template[i])
