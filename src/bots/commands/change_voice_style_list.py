from typing import Union

import discord

from src.json_utils.userdata import UserJson
from src.sbv2.models import ModelFolder, get_modelfolder_names

# style は 26個以上に対応させてないので、26個以上 style があるものを表示しようとすると多分エラーになる
class ChangeSpeakerView(discord.ui.View):
    def __init__(self, style_list: list[str], *, timeout: float | None = 180, model_name: str):
        super().__init__(timeout=timeout)

        select_item = [discord.SelectOption(label=i, value=f"{model_name}||{i}") for i in style_list]
        self.add_item(discord.ui.Select(options=select_item, custom_id="change_style", placeholder="使用したいスタイルを選択してください..."))


async def run(author: Union[discord.Member, discord.User]) -> tuple[discord.Embed, discord.ui.View]:
    action_user = UserJson(author.id)

    try:
        model_name = action_user.data["model_name"]
        modelfolder = ModelFolder(model_name)

    # もしそのユーザーのモデルが存在しないものならデフォルトモデルに書き換えておく
    except KeyError:
        folders: list[str] = get_modelfolder_names()
        action_user.data["model_name"] = folders[0]
        await action_user.async_write(action_user.data)

        model_name = action_user.data["model_name"]
        modelfolder = ModelFolder(model_name)

    style_list = modelfolder.styles

    description = f"1: {style_list[0]}"
    for i, val in enumerate(style_list):
        if i != 0:
            description += f"\n{i+1}: {val}"

    embed = discord.Embed(title=f"モデル: {model_name} の話者一覧", description=description)
    view = ChangeSpeakerView(style_list, model_name=model_name)

    return embed, view
