from io import BytesIO
from typing import Union
import discord

from src.sbv2.infer import infer_from_ctx
from src.json_utils.botdata import BotJson

bot_json = BotJson()
READ_LIMIT = bot_json.data['read_limit']


async def run(ctx: Union[discord.Message, discord.Interaction], *, text: str, ) -> tuple[str, BytesIO]:
    if len(text) >= (READ_LIMIT+5)*2:
        text = text[:READ_LIMIT*2]  # s!wavはREAD_LIMITの2倍まで許容しておく

    infer_bytes, _, _ = await infer_from_ctx(text, ctx)
    return f"\"{text}\"", infer_bytes
