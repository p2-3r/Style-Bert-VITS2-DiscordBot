import discord

from src.data import User
from src.bot import client


@client.event
async def on_interaction(ctx: discord.Interaction):
    try:
        if ctx.data['component_type'] == 2:
            await on_button_click(ctx)
        elif ctx.data['component_type'] == 3:
            await on_dropdown(ctx)
    except KeyError:
        pass


async def on_dropdown(ctx: discord.Interaction):
    action_user = User(ctx.user.id, username=ctx.user.name)
    choiced_val = ctx.data["values"][0]

    custom_id = ctx.data['custom_id']

    if custom_id == "change_model":
        action_user.write_userdata("model_name", choiced_val)
        action_user.write_userdata("speaker_name", "None")
        await ctx.response.send_message(f"使用するモデルを **{choiced_val}** に変更しました", ephemeral=True)

    elif custom_id == "change_speaker":
        # choiced_val: f"{model_name}||{speaker_name}"
        model_name, speaker_name = choiced_val.split("||")
        action_user.write_userdata("model_name", model_name)
        action_user.write_userdata("speaker_name", speaker_name)

        content = f"使用する話者を **{speaker_name}** に変更しました"
        if action_user.model_name != model_name:
            content = f"使用するモデルを **{action_user.model_name}** から **{model_name}** に変更しました。\n" + content

        await ctx.response.send_message(content, ephemeral=True)


async def on_button_click(ctx: discord.Interaction):
    pass
