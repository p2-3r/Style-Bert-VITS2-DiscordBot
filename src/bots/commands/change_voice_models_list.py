import discord

from src.sbv2.models import get_modelfolder_names_sep


class ChangeModelView(discord.ui.View):
    def __init__(self, model_list: list[str], *, timeout: float | None = 180,  add_pagebutton: bool):
        super().__init__(timeout=timeout)

        if add_pagebutton:
            [self.add_item(i) for i in [discord.ui.Button(label="<-", style=discord.ButtonStyle.primary, custom_id="model_pageback", disabled=True),   # type: ignore
                                        discord.ui.Button(label="0", style=discord.ButtonStyle.gray, disabled=True),
                                        discord.ui.Button(label="->", style=discord.ButtonStyle.primary, custom_id="model_pageforward")]]

        select_item = [discord.SelectOption(label=i, value=i) for i in model_list]
        self.add_item(discord.ui.Select(options=select_item, custom_id="change_model", placeholder="使用したいモデルを選択してください..."))


def run() -> tuple[discord.Embed, discord.ui.View]:
    model_list_list: list[list[str]] = get_modelfolder_names_sep(sep=25)

    # モデルが26個以上ならページ移動ボタンを追加
    if len(model_list_list) >= 2:
        add_pagebutton = True
    else:
        add_pagebutton = False

    # 25番目までのモデルを取得
    model_list = model_list_list[0]

    description = f"1: {model_list[0]}"
    for i, val in enumerate(model_list):
        if i != 0:
            description += f"\n{i+1}: {val}"

    embed = discord.Embed(title="使用できるモデル一覧", description=description)
    view = ChangeModelView(model_list, add_pagebutton=add_pagebutton)

    return embed, view
