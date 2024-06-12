from typing import Union
import asyncio
import io

from style_bert_vits2.tts_model import TTSModel  # type: ignore
from scipy.io import wavfile as scipy_wave  # type: ignore
import discord

from src.json_utils.userdata import UserJson
from src.json_utils.botdata import BotJson
from src.tools import text_replace

bot_json = BotJson()

# モデルをたくさん読みこみすぎてメモリを食わないように
# この変数たちに保存しておいて、MODELS_UPPERLIMIT の数を超えると
# 一番使用されてないモデルを消去して新しいモデルを追加するようにしている
# (正直意味あるかはわからない)

# 辞書だと順番が保持されないので順番は models_order リストで管理、
# 実際のTTSModelクラスは ttsmodels 辞書に置いておく
ttsmodels: dict[str, TTSModel] = {}
models_order: list[str] = []

MODELS_UPPERLIMIT = bot_json.data['models_upperlimit']
DEVICE = bot_json.data['device']


async def infer_from_ctx(infer_text: str, ctx: Union[discord.Message, discord.Interaction], *, replace: bool = False):
    # 戻り値の型ヒントを書くのがめんどくさいので書いてない
    """
    ctx (メッセージまたはスラッシュコマンドの入力) に基づいて音声を生成する。

    ctx の送信者のモデル設定をjsonから取り出してその設定を使用する。

    キーワード引数:
        replace (bool): True に設定すると、サーバー辞書などを使用した置換が行われる。
    """

    if replace:
        infer_text = text_replace.replace_text_all(infer_text, ctx=ctx)

    if isinstance(ctx, discord.Message):
        user_id = ctx.author.id
    elif isinstance(ctx, discord.Interaction):
        user_id = ctx.user.id
    else:
        raise AssertionError("Discord.Message or discord.Interaction can be specified for the argument ctx.")

    user = UserJson(user_id)

    # 使用されたら、models_order の一番先頭に持ってきておく
    if user.model_safetensor.stem in models_order:
        models_order.pop(models_order.index(user.model_safetensor.stem))
    models_order.insert(0, user.model_safetensor.stem)

    # MODELS_UPPERLIMIT の数を超えたら、一番古いものを削除する
    if len(models_order) > MODELS_UPPERLIMIT:
        pop_val = models_order.pop(-1)
        del ttsmodels[pop_val]

    # もしモデルがttsmodelsに存在しないものだったら読み込む
    if str(user.model_safetensor.stem) not in ttsmodels.keys():
        ttsmodels[str(user.model_safetensor.stem)] = TTSModel(
            user.model_safetensor, user.model_json, user.model_npy, device=DEVICE
        )

    # ttsmodelsに登録しておいた TTSModel を持ってくる
    infer_model = ttsmodels[str(user.model_safetensor.stem)]

    speaker_id = infer_model.spk2id[f"{user.model_speaker}"]

    sr, audio = await asyncio.to_thread(infer_model.infer, infer_text, speaker_id=speaker_id, style=user.model_style)

    # BytesIO を使ってファイルに保存せずに渡す
    infer_bytes = io.BytesIO()
    scipy_wave.write(infer_bytes, sr, audio)  # type: ignore

    return infer_bytes, sr, audio
