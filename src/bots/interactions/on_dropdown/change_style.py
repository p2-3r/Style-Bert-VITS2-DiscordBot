import discord

from src.json_utils.userdata import UserJson


async def run(ctx: discord.Interaction) -> None:
    action_user = UserJson(ctx.user.id)
    choiced_val = ctx.data["values"][0]  # type: ignore

    await ctx.response.defer()

    # choiced_val: f"{model_name}||{style_name}"
    choiced_model_name, choiced_style_name = choiced_val.split("||")  # type: ignore

    # 返答用文章作成
    content = f"使用する話者を **{choiced_style_name}** に変更しました"
    if action_user.data["model_name"] != choiced_model_name:
        content = f"使用するモデルを **{action_user.data['model_name']}** から **{choiced_model_name}** に変更しました。\n" + content

    # dataとjsonをそれぞれ書き換え
    action_user.data["model_name"] = choiced_model_name
    action_user.data["style"] = choiced_style_name
    await action_user.async_write(action_user.data)

    await ctx.followup.send(content, ephemeral=True)
