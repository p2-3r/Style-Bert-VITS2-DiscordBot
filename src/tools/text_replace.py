import re
from typing import Union

import discord

from src.json_utils.serverdata import ServerJson
from src.global_data import client
from src.tools import engtokana


class TextReplace():
    @classmethod
    def removes(cls, content: str) -> str:
        """
        コードブロックや、絵文字などを消去する
        """

        if "```" in content:
            content = "コードブロック"

        replace_dict = {"<:.+:.+>": "",
                        "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+": "\nユーアールエル\n",  # type: ignore
                        r"`.*?`": "コード",
                        r"<.*?>": ""}

        for before, after in replace_dict.items():  # replace_dict の key を value に置き換える
            content = re.sub(before, after, content)

        return content

    @classmethod
    def mention_to_username(cls, content: str, client: discord.Client) -> str:
        mention_list = re.findall("<@[0-9]+>", content)
        if mention_list:
            userid_list = [int(re.findall("[0-9]+", i)[0]) for i in mention_list]
            username_list = ["不明なユーザー" if i == None else i.display_name for i in [client.get_user(i) for i in userid_list]]

            for mention, username in zip(mention_list, username_list):
                content = content.replace(mention, username, 1)

        return content

    @classmethod
    def server_dict(cls, content: str, server_id: int) -> str:

        server = ServerJson(server_id)
        server_dict: dict[str, str] = server.data["dic"]

        if server_dict:
            read_list: list[str] = []
            for i, k in enumerate(list(server_dict.keys())):
                content = content.replace(k, f"{{{str(i)}}}")
                read_list.append(server_dict[k])

            content = content.format(*read_list)

        return content


def replace_text_all(content: str, *, ctx: Union[discord.Message, discord.Interaction]) -> str:

    if ctx.guild is None:
        raise AssertionError("guild is None")

    guild = ctx.guild

    content = TextReplace.mention_to_username(content, client)
    content = TextReplace.removes(content)
    content = TextReplace.server_dict(content, guild.id)
    content = engtokana.convert_all_text_kana(content)

    if content == "":  # 何もないとバグるので
        content = "メッセージ"

    return content
