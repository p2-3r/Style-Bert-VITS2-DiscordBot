from pathlib import Path
from typing import TypedDict

from src.json_utils.read_write import JsonFile

serverdata_folder = Path("./jsondatas/servers")


class ServerJsonType(TypedDict):
    dic: dict[str, str]
    dic_onlyadmin: bool
    auto_join: int | None


class ServerJson:
    """
    `./jsondatas/servers` から指定したユーザーIDの

    jsonファイルを取り出して `self.data` に保存する。

    もしjsonファイルが存在しなければ、jsonを新しく作成する。
    """

    server_id: int
    json: JsonFile
    data: ServerJsonType

    serverdict_template: ServerJsonType = {"dic": {},
                                           "dic_onlyadmin": True,
                                           "auto_join": None}

    def __init__(self, server_id: int) -> None:
        self.server_id = server_id

        server_jsonpath = serverdata_folder / f"{server_id}.json"

        # もしサーバーデータが作成されていなければ作成する
        if not server_jsonpath.exists():
            self.json = JsonFile(server_jsonpath)
            self.json.write(self.serverdict_template)
        else:
            self.json = JsonFile(server_jsonpath)

        self.data = self.json.read()

    async def keycheck_add(self) -> None:
        """
        server_templateと比較して、もし足らないキーがあれば追加するメソッド
        """

        flag = False
        for i in self.serverdict_template.keys():
            datakeys = self.data.keys()
            if i not in datakeys:
                self.data[i] = self.serverdict_template[i]
                flag = True

        if flag:
            await self.async_write(self.data)

    async def async_read(self) -> ServerJsonType:
        return ServerJsonType(await self.json.async_read())

    async def async_write(self, data: ServerJsonType):
        await self.json.async_write(data)

    # 変換前と変換後を指定してサーバー辞書に読み方を登録する
    async def write_dic(self, before: str, after: str):
        self.data["dic"][before] = after
        await self.async_write(self.data)

    # 変換前を指定してサーバー辞書から登録した読み方を削除する
    async def delete_dic(self, before: str):
        try:
            self.data["dic"].pop(before)
        except KeyError:
            raise KeyError("The key does not exist in the server dictionary.")

        await self.async_write(self.data)
