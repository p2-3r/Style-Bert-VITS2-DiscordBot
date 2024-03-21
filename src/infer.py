from typing import Optional, Union
import typing
from pathlib import Path
import asyncio
import io

from scipy.io import wavfile as scipy_wave
import discord

from src.data import User, botdata
from src.model import DEBUG

DEVICE = botdata.read_all()["device"]

ttsmodels = {}
models_order = []
models_upperlimit: int = botdata.read_all()["models_upperlimit"]

if DEBUG:
    async def user_infer(text: str, ctx: Union[discord.Message, discord.Interaction]):
        return

if not DEBUG:
    from style_bert_vits2.tts_model import TTSModel

    async def user_infer(text: str, ctx: Union[discord.Message, discord.Interaction]):

        if isinstance(ctx, discord.Message):
            text = text
            user_id = ctx.author.id
            user_name = ctx.author.name
        elif isinstance(ctx, discord.Interaction):
            pass  # TODO 後で書く

        else:
            raise Exception("Discord.Message or discord.Interaction can be specified for the argument ctx.")

        user = User(user_id, user_name)

        if user.safetensor.stem in models_order:
            models_order.pop(models_order.index(user.safetensor.stem))
        models_order.insert(0, user.safetensor.stem)

        if len(models_order) > models_upperlimit:
            pop_val = models_order.pop(-1)
            del ttsmodels[pop_val]

        if not str(user.safetensor.stem) in ttsmodels.keys():
            ttsmodels[str(user.safetensor.stem)] = TTSModel(user.safetensor, user.json, user.npy, device=DEVICE)

        infer_model: TTSModel = ttsmodels[str(user.safetensor.stem)]

        sr, audio = await asyncio.to_thread(infer_model.infer, text)

        bytes_ = io.BytesIO()
        scipy_wave.write(bytes_, sr, audio)
        print(bytes_.getvalue())

        return bytes_
