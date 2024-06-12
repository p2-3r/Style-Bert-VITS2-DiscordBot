from typing import Union

import discord

from src.sbv2.models import ModelFolder, get_modelfolder_names, get_speaker_names_sep
from src.json_utils.userdata import UserJson


class ChangeSpeakerView(discord.ui.View):
    def __init__(self, speaker_list: list[str], *, timeout: float | None = 180, add_pagebutton: bool, model_name: str):
        super().__init__(timeout=timeout)

        if add_pagebutton:
            [self.add_item(i) for i in [discord.ui.Button(label="<-", style=discord.ButtonStyle.primary, custom_id="speaker_pageback", disabled=True),  # type: ignore
                                        discord.ui.Button(label="0", style=discord.ButtonStyle.gray, disabled=True),
                                        discord.ui.Button(label="->", style=discord.ButtonStyle.primary, custom_id="speaker_pageforward")]]

        select_item = [discord.SelectOption(label=i, value=f"{model_name}||{i}") for i in speaker_list]
        self.add_item(discord.ui.Select(options=select_item, custom_id="change_speaker", placeholder="使用したい話者を選択してください..."))


async def run(author: Union[discord.Member, discord.User]) -> tuple[discord.Embed, discord.ui.View]:
    action_user = UserJson(author.id)

    try:
        modelfolder = ModelFolder(action_user.data["model_name"])
        model_name = action_user.data["model_name"]
        speaker_list_list = get_speaker_names_sep(modelfolder, sep=25)

    # もしそのユーザーのモデルが存在しないものならデフォルトモデルに書き換えておく
    except KeyError:
        folders: list[str] = get_modelfolder_names()
        action_user.data["model_name"] = folders[0]
        await action_user.async_write(action_user.data)

        modelfolder = ModelFolder(action_user.data["model_name"])
        model_name = action_user.data["model_name"]
        speaker_list_list = get_speaker_names_sep(modelfolder, sep=25)

    # モデルが26個以上ならページ移動ボタンを追加
    if len(speaker_list_list) >= 2:
        add_pagebutton = True
    else:
        add_pagebutton = False

    speaker_list = speaker_list_list[0]

    description = f"1: {speaker_list[0]}"
    for i, val in enumerate(speaker_list):
        if i != 0:
            description += f"\n{i+1}: {val}"

    embed = discord.Embed(title=f"モデル: {model_name} の話者一覧", description=description)
    view = ChangeSpeakerView(speaker_list, add_pagebutton=add_pagebutton, model_name=model_name)

    return embed, view
