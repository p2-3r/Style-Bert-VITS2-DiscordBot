from pathlib import Path
from glob import glob
import re

from style_bert_vits2.tts_model import TTSModel  # type: ignore
from style_bert_vits2.nlp import bert_models  # type: ignore
from style_bert_vits2.constants import Languages  # type: ignore
from style_bert_vits2.nlp.japanese.g2p_utils import g2kata_tone  # type: ignore
from style_bert_vits2.nlp.japanese.normalizer import normalize_text  # type: ignore

assets_root = Path("model_assets")


def get_modelfolder_names() -> list[str]:
    """
    model_assets フォルダにある、中にちゃんと config.jsonなどが入っているフォルダだけ返す
    """

    globs = glob(str(assets_root) + "/**/")
    folder_paths = [Path(i) for i in globs]

    model_names: list[str] = []
    for i in folder_paths:
        config_json = (i / "config.json").exists()
        vectors_npy = (i / "style_vectors.npy").exists()
        model_safetensors = len(list(i.glob("*.safetensors")))

        if all([config_json, vectors_npy, model_safetensors]):
            model_names.append(i.name)

    return model_names


def get_modelfolder_names_sep(*, sep: int) -> list[list[str]]:
    """
    model_assets フォルダにある、中にちゃんと config.jsonなどが入っているフォルダを、

    modelfolder の名前を指定した sep の数で区切って `list[list[str]]` として返す
    """

    if sep <= 0:
        raise ValueError("'sep' value must be at least 1.")

    model_names = get_modelfolder_names()
    model_len = len(model_names)

    sep_model_names: list[list[str]] = []

    if model_len > sep:
        templist = []
        for i in range(model_len // sep):
            sep_model_names.append(model_names[0 + (i * sep): sep + (i * sep)])

        if (mod := model_len % sep) != 0:
            sep_model_names.append(model_names[-mod:])

        model_names = templist
    else:
        sep_model_names = [model_names]

    return sep_model_names


class ModelFolder:
    """
    model_assets フォルダ内のフォルダ名でモデルを指定する。

    もし指定したモデル名が存在しない場合は KeyError を返す。
    """

    def __init__(self, model_name: str) -> None:
        modelfolder_names = get_modelfolder_names()

        if model_name in modelfolder_names:
            self.name = model_name
            self.model_folder_path = assets_root / self.name
        else:
            raise KeyError("That model doesn't exist.")

    @property
    def safetensors(self) -> list[Path]:
        """
        モデルフォルダ内にあるすべての safetensors Path をリストで返す。
        """

        g = glob(str(self.model_folder_path) + "/*.safetensors")
        safetensors = [Path(i) for i in g]
        return safetensors

    @property
    def latest_safetensors(self) -> Path:
        """
        モデルフォルダ内の一番ステップ数が大きい safetensors のパスを返す。

        もし [モデル名]_e[エポック数]_s[ステップ数].safetensors 形式の

        safetensors が存在しなければ、一番後ろの safetensors を返す。
        """

        re_safetensors = [
            i
            for i in self.safetensors
            if re.match(".+_e[0-9]+_s[0-9]+.safetensors", i.name)
        ]

        if re_safetensors:
            stem = [i.stem for i in re_safetensors]
            step = [int(i.split("_s")[-1]) for i in stem]
            index = step.index(max(step))
            return re_safetensors[index]
        else:
            return self.safetensors[-1]

    @property
    def json(self) -> Path:
        return self.model_folder_path / "config.json"

    @property
    def npy(self) -> Path:
        return self.model_folder_path / "style_vectors.npy"

    @property
    def speakers(self) -> list[str]:
        model = TTSModel(
            model_path=self.latest_safetensors,
            config_path=self.json,
            style_vec_path=self.npy,
            device="cpu",
        )

        return list(model.id2spk.values())

    @property
    def styles(self) -> list[str]:
        model = TTSModel(
            model_path=self.latest_safetensors,
            config_path=self.json,
            style_vec_path=self.npy,
            device="cpu",
        )

        return list(model.style2id.keys())


def get_speaker_names_sep(modelfolder: ModelFolder, *, sep: int) -> list[list[str]]:
    """
    渡した ModelFolder の Speaker を sep の数で区切って `list[list[str]]` として返す
    """

    if sep <= 0:
        raise ValueError("'sep' value must be at least 1.")

    speaker_list = modelfolder.speakers

    speaker_len = len(speaker_list)

    if speaker_len > sep:
        templist: list[list[str]] = []
        for i in range(speaker_len // sep):
            templist.append(speaker_list[0 + (i * sep): sep + (i * sep)])

        if (mod := speaker_len % sep) != 0:
            templist.append(speaker_list[-mod:])

        speaker_list = templist

    else:
        speaker_list = [speaker_list]

    return speaker_list
