import re
from typing import Union

import discord

from src.data import Server
from src.bot import client


class Replace():
    @classmethod
    def emoji_other(cls, content: str) -> str:
        replace_dict = {'<:.+:.+>': '',
                        "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+": '\nユーアールエル\n',
                        "```(.|\n)+```": "\nコードブロック\n",
                        "'.+'": "コード"}

        for before, after in replace_dict.items():
            content = re.sub(before, after, content)
        return content

    @classmethod
    def mention2username(cls, content: str) -> str:
        mention_list = re.findall("<@[0-9]+>", content)
        if mention_list:
            userid_list = [int(re.findall("[0-9]+", i)[0]) for i in mention_list]
            username_list = ["不明なユーザー" if i == None else i.display_name for i in [client.get_user(i) for i in userid_list]]

            for mention, username in zip(mention_list, username_list):
                content = content.replace(mention, username, 1)

        return content

    @classmethod
    def server_dict(cls, content: str, server_id: int) -> str:

        server = Server(server_id)
        server_dict: dict[str, str] = server.data["dic"]

        if server_dict:
            read_list = []
            for i, k in enumerate(list(server_dict.keys())):
                content = content.replace(k, f"{{{str(i)}}}")
                read_list.append(server_dict[k])

            content = content.format(*read_list)

        return content


def replace_text(content: str, *, ctx: Union[discord.Message, discord.Interaction]) -> str:

    if isinstance(ctx, discord.Message):
        guild = ctx.guild
    elif isinstance(ctx, discord.Interaction):
        guild = ctx.guild

    content = Replace.emoji_other(content)
    content = Replace.mention2username(content)
    content = Replace.server_dict(content, guild.id)
    return content
