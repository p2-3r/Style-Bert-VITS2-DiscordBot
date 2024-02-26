import re

import discord

import data as f_data

class Replace():
    def emoji_other(self, content) -> str:
        replace_dict = {'<:.+:.+>': '',
                        "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+": '、url、',
                        "```(.|\n)+```": "、コードブロック、"}

        for before, after in replace_dict.items():
            content = re.sub(before, after, content)
        return content

    def mention2username(self, content: str, client: discord.Client) -> str:
        mention_list = re.findall("<@[0-9]+>", content)
        if mention_list:
            userid_list = [int(re.findall("[0-9]+", i)[0]) for i in mention_list]
            username_list = ["不明なユーザー" if i == None else i.display_name for i in [client.get_user(i) for i in userid_list]]

            for mention, username in zip(mention_list, username_list):
                content = content.replace(mention, username, 1)

        return content

    def server_dict(self, content: str, server_id: int) -> str:
        server_dict = f_data.read_server_dict(server_id)

        if server_dict:
            read_list = []
            for i, k in enumerate(list(server_dict.keys())):
                content = content.replace(k, f"{{{str(i)}}}")
                read_list.append(server_dict[k])

            content = content.format(*read_list)

        return content

replace = Replace()

def replace_text(content: str, client: discord.Client, server_id: int) -> str:
    content = replace.emoji_other(content)
    content = replace.mention2username(content, client)
    content = replace.server_dict(content, server_id)
    return content

