import discord

from src.bots.interactions.on_dropdown import change_model, change_server_settings, change_speaker, change_style
from src.bots.interactions.on_button_click import dict_add, dict_remove, model_pageback, model_pageforward, speaker_pageback, speaker_pageforward


# interaction (ボタンやリスト選択など) に関する処理
def register(client: discord.Client):

    @client.event
    async def on_interaction(ctx: discord.Interaction):  # type: ignore
        try:
            if ctx.data['component_type'] == 2:  # type: ignore
                await on_button_click(ctx)
            elif ctx.data['component_type'] == 3:  # type: ignore
                await on_dropdown(ctx)
        except KeyError:
            pass

"""
ここではどのボタンやプルダウンが操作されたかによる分岐だけ書いて、
実際の動作は src.bots.interactions の、
on_button_click と on_dropdown フォルダに置いてある
"""

async def on_dropdown(ctx: discord.Interaction):
    custom_id = ctx.data['custom_id']  # type: ignore

    if custom_id == "change_model":
        await change_model.run(ctx)

    elif custom_id == "change_speaker":
        await change_speaker.run(ctx)

    elif custom_id == "change_style":
        await change_style.run(ctx)

    elif custom_id == "change_server_settings":
        await change_server_settings.run(ctx)

    else:  # バグが起きない限り実行されない
        raise AssertionError(f"Error: {custom_id=}")


async def on_button_click(ctx: discord.Interaction):
    custom_id = ctx.data['custom_id']  # type: ignore

    if custom_id == "dict_add":
        await dict_add.run(ctx)

    elif custom_id == "dict_remove":
        await dict_remove.run(ctx)

    elif custom_id == "model_pageforward":
        await model_pageforward.run(ctx)

    elif custom_id == "model_pageback":
        await model_pageback.run(ctx)

    elif custom_id == "speaker_pageforward":
        await speaker_pageforward.run(ctx)

    elif custom_id == "speaker_pageback":
        await speaker_pageback.run(ctx)

    else:  # バグが起きない限り実行されない
        raise AssertionError(f"Error: {custom_id=}")
