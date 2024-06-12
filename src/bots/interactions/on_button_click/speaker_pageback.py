import discord

from src.sbv2.models import ModelFolder, get_speaker_names_sep


class ChangeSpeakerView(discord.ui.View):
    def __init__(self, speaker_list_list: list[list[str]], *, timeout: float | None = 180, current_page: int, model_name: str):
        super().__init__(timeout=timeout)

        speaker_list = speaker_list_list[current_page-1]

        # もし現在のページが一番最初なら、前のページへ行くボタンを無効化する
        if current_page != len(speaker_list_list):
            is_exist_backpage = False
        else:
            is_exist_backpage = True

        [self.add_item(i) for i in [discord.ui.Button(label="<-", style=discord.ButtonStyle.primary, custom_id="speaker_pageback", disabled=False),  # type: ignore
                                    discord.ui.Button(label=f"{current_page-1}", style=discord.ButtonStyle.gray, disabled=True),
                                    discord.ui.Button(label="->", style=discord.ButtonStyle.primary, custom_id="speaker_pageforward", disabled=is_exist_backpage)]]

        # 選択されたときの処理先:
        """ src.bots.interactions.on_dropdown.change_speaker.run """
        select_item = [discord.SelectOption(label=i, value=f"{model_name}||{i}") for i in speaker_list]
        self.add_item(discord.ui.Select(options=select_item, custom_id="change_speaker", placeholder="使用したい話者を選択してください..."))


async def run(ctx: discord.Interaction) -> None:
    # 何ページ目かと、何のモデルのページなのかを embed から取得する
    description_f = int(ctx.message.embeds[0].description.split(":", maxsplit=1)[0])  # type: ignore
    model_name = ctx.message.embeds[0].title.split("モデル: ")[1].split(" の話者一覧")[0]  # type: ignore

    current_page = description_f // 25

    modelfolder = ModelFolder(model_name)
    speaker_list_list = get_speaker_names_sep(modelfolder, sep=25)

    speaker_list = speaker_list_list[current_page-1]

    description = f"{1 + (current_page-1)*25}: {speaker_list[0]}"
    for i, val in enumerate(speaker_list):
        if i != 0:
            description += f"\n{(i+1)+(current_page-1)*25}: {val}"

    embed = discord.Embed(title=f"モデル: {model_name} の話者一覧", description=description)
    view = ChangeSpeakerView(speaker_list_list, current_page=current_page, model_name=model_name)

    await ctx.response.send_message(embed=embed, view=view)
    await ctx.message.delete()  # type: ignore
