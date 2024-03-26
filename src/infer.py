from typing import Union
import asyncio
import io

from scipy.io import wavfile as scipy_wave
import discord

from src.commands.slash import speaker
from src import replace_text
from src.bot import DEVICE
from src.data import User, botdata
from src.model import DEBUG

ttsmodels = {}
models_order = []
models_upperlimit: int = botdata.read_all()["models_upperlimit"]

if DEBUG:

    async def user_infer(text: str, ctx: Union[discord.Message, discord.Interaction], *, replace: bool = False):
        raise AssertionError("DEBUG variable is set to True.")


if not DEBUG:
    from style_bert_vits2.tts_model import TTSModel

    async def user_infer(text: str, ctx: Union[discord.Message, discord.Interaction], *, replace: bool = False):

        # replace引数がTrueならサーバー辞書などでtextを変換する
        if replace:
            text = replace_text.replace_text(text, ctx=ctx)

        if isinstance(ctx, discord.Message):
            user_id = ctx.author.id
            user_name = ctx.author.name
        elif isinstance(ctx, discord.Interaction):
            user_id = ctx.user.id
            user_name = ctx.user.name

        else:
            raise Exception("Discord.Message or discord.Interaction can be specified for the argument ctx.")

        user = User(user_id, user_name)

        if user.safetensor.stem in models_order:
            models_order.pop(models_order.index(user.safetensor.stem))
        models_order.insert(0, user.safetensor.stem)

        if len(models_order) > models_upperlimit:
            pop_val = models_order.pop(-1)
            del ttsmodels[pop_val]

        if str(user.safetensor.stem) not in ttsmodels.keys():
            ttsmodels[str(user.safetensor.stem)] = TTSModel(
                user.safetensor, user.json, user.npy, device=DEVICE
            )

        infer_model: TTSModel = ttsmodels[str(user.safetensor.stem)]

        speaker_id = infer_model.spk2id[f"{user.speaker}"]

        sr, audio = await asyncio.to_thread(infer_model.infer, text, speaker_id=speaker_id, style=user.style)

        bytes_ = io.BytesIO()
        scipy_wave.write(bytes_, sr, audio)

        return bytes_, sr, audio
