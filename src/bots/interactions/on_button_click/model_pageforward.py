import discord

from src.sbv2.models import get_modelfolder_names_sep


class ChangeModelView(discord.ui.View):
    def __init__(self, model_list_list: list[list[str]], *, timeout: float | None = 180, current_page: int):
        super().__init__(timeout=timeout)

        model_list = model_list_list[current_page+1]

        # もし現在のページが一番最後なら、次のページへ行くボタンを無効化する
        if (current_page+2) != len(model_list_list):
            is_exist_forwardpage = False
        else:
            is_exist_forwardpage = True

        [self.add_item(i) for i in [discord.ui.Button(label="<-", style=discord.ButtonStyle.primary, custom_id="model_pageback", disabled=False),  # type: ignore
                                    discord.ui.Button(label=f"{current_page+1}", style=discord.ButtonStyle.gray, disabled=True),
                                    discord.ui.Button(label="->", style=discord.ButtonStyle.primary, custom_id="model_pageforward", disabled=is_exist_forwardpage)]]

        # 選択されたときの処理先:
        """ src.bots.interactions.on_dropdown.change_model.run """
        select_item = [discord.SelectOption(label=i, value=i) for i in model_list]
        self.add_item(discord.ui.Select(options=select_item, custom_id="change_model", placeholder="使用したいモデルを選択してください..."))


async def run(ctx: discord.Interaction) -> None:

    # 現在何ページ目かをembedの内容から求める
    description_f = int(ctx.message.embeds[0].description.split(":", maxsplit=1)[0])  # type: ignore
    current_page = description_f // 25

    model_list_list: list[list[str]] = get_modelfolder_names_sep(sep=25)

    model_list = model_list_list[current_page+1]

    description = f"{1 + (current_page+1)*25}: {model_list[0]}"
    for i, val in enumerate(model_list):
        if i != 0:
            description += f"\n{(i+1)+(current_page+1)*25}: {val}"

    embed = discord.Embed(title="使用できるモデル一覧", description=description)
    view = ChangeModelView(model_list_list, current_page=current_page)

    await ctx.response.send_message(embed=embed, view=view)
    await ctx.message.delete()  # type: ignore
