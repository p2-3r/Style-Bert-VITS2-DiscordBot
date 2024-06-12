from typing import Union

import discord

from src.json_utils.userdata import UserJson


async def run(ctx: Union[discord.Message, discord.Interaction], *, input_num: float):
    if isinstance(ctx, discord.Message):
        user = UserJson(ctx.author.id)
    elif isinstance(ctx, discord.Interaction):
        user = UserJson(ctx.user.id)
    else:
        raise AssertionError("NoneError")

    # 0.1 ~ 5.0 の範囲外ならその範囲に収める
    if input_num < 0.1:
        input_num = 0.1
    elif input_num > 5.0:
        input_num = 5.0

    # 小数点以下1桁までに制限する
    input_num = round(input_num, 1)

    user.data["length"] = input_num
    await user.async_write(user.data)

    return f"読み上げ速度を **{input_num}** に変更しました。"
