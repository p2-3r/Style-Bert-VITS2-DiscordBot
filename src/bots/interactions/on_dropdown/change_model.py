import discord

from src.json_utils.userdata import UserJson


async def run(ctx: discord.Interaction) -> None:
    action_user = UserJson(ctx.user.id)
    choiced_model_name = ctx.data["values"][0]  # type: ignore

    await ctx.response.defer()

    # ユーザーのデータとjsonファイルをそれぞれ書き換え
    action_user.data["model_name"] = choiced_model_name
    action_user.data["speaker_name"] = "None"        # 存在していない話者を指定しても読み込み時に
    await action_user.async_write(action_user.data)  # 自動的に存在するものに変えてくれるので "None" 指定で大丈夫

    await ctx.followup.send(f"使用するモデルを **{choiced_model_name}** に変更しました", ephemeral=True)
