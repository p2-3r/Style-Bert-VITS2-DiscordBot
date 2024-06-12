from copy import deepcopy
from pathlib import Path
from typing import TypedDict


from src.sbv2.models import ModelFolder, get_modelfolder_names
from src.json_utils.read_write import JsonFile
from src.json_utils.botdata import BotJson

bot_json = BotJson()
bot_json_data = bot_json.read()

userdata_folder = Path("./jsondatas/users")


# 読み込んだデータの型ヒント
class UserJsonType(TypedDict):
    model_name: str
    speaker_name: str
    style: str
    length: float


# Userの設定ファイル読み込み用クラス
class UserJson:
    """
    `./jsondatas/users` から指定したユーザーIDの

    jsonファイルを取り出して `self.data` に保存する。

    もしjsonファイルが存在しなければ、`self.data`、各モデル情報は

    テンプレートが使用される。

    Attributes
    -
        user_id: discordのユーザーID
        json: src.json_utils.read_write.JsonFile Class
        data: UserJsonType (TypedDict)

    以下はこのユーザーのモデル設定
        model_safetensor: Path
        model_speaker: str
        model_style: str
        model_json: Path
        model_npy: Path
        model_length: float
    """

    user_id: int
    json: JsonFile | None
    data: UserJsonType

    model_safetensor: Path
    model_name: str
    model_speaker: str
    model_style: str
    model_json: Path
    model_npy: Path
    model_length: float

    userdict_template: UserJsonType = {
        "model_name": "None",
        "speaker_name": "None",
        "style": "None",
        "length": 1.0,
    }

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        user_jsonpath = userdata_folder / f"{user_id}.json"

        # ユーザーがuser_dataに存在するならそのデータ、ないならテンプレートのデータをセットする
        if user_jsonpath.exists():
            self.json = JsonFile(user_jsonpath)
            self.data = self.json.read()
        else:
            self.json = None
            self.data = deepcopy(self.userdict_template)

        # もしそのモデル名が存在しないならモデルフォルダの一番上を選択する
        # jsonファイルがあるなら存在しないモデル名を存在するモデル名に書き換えておく
        try:
            modelfolder = ModelFolder(self.data["model_name"])
            self.data["model_name"] = modelfolder.name
            self.model_name = modelfolder.name
        except KeyError:
            modelfolder_names = get_modelfolder_names()
            modelfolder = ModelFolder(modelfolder_names[0])
            self.model_name = modelfolder_names[0]

            if self.json is not None:
                self.data["model_name"] = modelfolder_names[0]
                self.json.write(self.data)

        # もしその話者が存在しないなら一番最初のものを選択 jsonファイルがあるなら書き換える
        modelfolder_speakers = modelfolder.speakers
        self.model_speaker = self.data["speaker_name"]
        if not self.data["speaker_name"] in modelfolder_speakers:
            self.data["speaker_name"] = modelfolder_speakers[0]
            self.model_speaker = modelfolder_speakers[0]
            if self.json is not None:
                self.json.write(self.data)

        # もしそのスタイル名が存在しないならニュートラルまたは一番最初を選択
        if self.data["style"] in modelfolder.styles:
            self.model_style = self.data["style"]
        else:
            modelfolder_styles = modelfolder.styles

            if "Neutral" in modelfolder_styles:
                self.model_style = "Neutral"
                self.data["style"] = "Neutral"
            else:
                self.model_style = modelfolder_styles[0]
                self.data["style"] = modelfolder_styles[0]

            if self.json is not None:
                self.json.write(self.data)

        # ユーザーのモデル情報設定
        self.model_safetensor = modelfolder.latest_safetensors
        self.model_json = modelfolder.json
        self.model_npy = modelfolder.npy
        self.model_length: float = self.data["length"]

    async def keycheck_add(self) -> None:
        """
        userdict_templateと比較して、もし足らないキーがあれば追加するメソッド
        """

        flag = False
        for i in self.userdict_template.keys():
            datakeys = self.data.keys()
            if i not in datakeys:
                self.data[i] = self.userdict_template[i]
                flag = True

        if flag:
            await self.async_write(self.data)

    async def create(self) -> None:
        """
        `./jsondatas/users` に、このユーザーのjsonファイルを新しく作成する。
        """

        self.json = JsonFile(userdata_folder / f"{self.user_id}.json")
        await self.async_write(self.userdict_template)

    async def async_read(self) -> UserJsonType:
        if self.json is None:
            raise AssertionError("self.json is None")
        else:
            return UserJsonType(await self.json.async_read())

    async def async_write(self, data: UserJsonType) -> None:
        if self.json is None:
            await self.create()  # もし self.json が存在しないなら、self.json を作成してから書き込む

        await self.json.async_write(data)   # type: ignore
