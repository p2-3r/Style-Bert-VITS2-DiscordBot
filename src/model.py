from pathlib import Path
from glob import glob
import re
from typing import Union, Optional

DEBUG = False

if not DEBUG:
    from style_bert_vits2.tts_model import TTSModel
    from style_bert_vits2.nlp import bert_models
    from style_bert_vits2.constants import Languages
    from style_bert_vits2.nlp.japanese.g2p_utils import g2kata_tone
    from style_bert_vits2.nlp.japanese.normalizer import normalize_text

    bert_models.load_model(Languages.JP, "ku-nlp/deberta-v2-large-japanese-char-wwm")
    bert_models.load_tokenizer(Languages.JP, "ku-nlp/deberta-v2-large-japanese-char-wwm")

    class Load:
        @classmethod
        def model(cls, *, model_file: Path, config_file: Path, style_file: Path, device: str = "cuda"):
            model = TTSModel(
                model_path=model_file,
                config_path=config_file,
                style_vec_path=style_file,
                device=device,
            )
            return model

    class Model_Get:
        @classmethod
        def speakers(cls, model: TTSModel) -> list[str]:
            return list(model.id2spk.values())

        @classmethod
        def styles(cls, model: TTSModel) -> list[str]:
            return list(model.style2id.keys())

    def g2k(text: str):
        normalized = normalize_text(text)
        return g2kata_tone(normalized)


assets_root = Path("model_assets")


class ModelFolder:
    def __init__(self, model_name: str) -> None:
        g = glob(str(assets_root) + "/**/")
        folder_names = [Path(i) for i in g]

        model_names = []
        for i in folder_names:
            config_json = (i / "config.json").exists()
            vectors_npy = (i / "style_vectors.npy").exists()
            model_safetensors = len(list(i.glob("*.safetensors")))

            if all([config_json, vectors_npy, model_safetensors]):
                model_names.append(i.name)

        if model_name in model_names:
            self.name = model_name
            self.model_folder_path = assets_root / self.name
        else:
            raise KeyError("That model doesn't exist.")

    @property
    def safetensors(self) -> list[Path]:
        g = glob(str(self.model_folder_path) + "/*.safetensors")
        safetensors = [Path(i) for i in g]
        return safetensors

    @property
    def latest_safetensors(self) -> Path:
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
        if not DEBUG:
            model = TTSModel(
                model_path=self.latest_safetensors,
                config_path=self.json,
                style_vec_path=self.npy,
                device="cpu",
            )

            return Model_Get.speakers(model)

        return ["RinneElu", "jvnv-F1-jp"]

    @property
    def styles(self) -> list[str]:
        if not DEBUG:
            model = TTSModel(
                model_path=self.latest_safetensors,
                config_path=self.json,
                style_vec_path=self.npy,
                device="cpu",
            )

            return Model_Get.styles(model)
        return ["Neutral", "Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise"]


def get_modelfolders(*, sep: Optional[int] = None) -> Union[list[str], list[list[str]]]:
    g = glob(str(assets_root) + "/**/")
    folder_names = [Path(i) for i in g]

    model_names = []
    for i in folder_names:
        config_json = (i / "config.json").exists()
        vectors_npy = (i / "style_vectors.npy").exists()
        model_safetensors = len(list(i.glob("*.safetensors")))

        if all([config_json, vectors_npy, model_safetensors]):
            model_names.append(i.name)

    # sepに値が入っていた場合model_namesをsepの値で分割したリストを返す
    if sep is not None:
        if sep <= 0:
            raise ValueError("'sep' value must be at least 1.")

        model_len = len(model_names)
        if model_len > sep:
            templist = []
            for i in range(model_len // sep):
                templist.append(model_names[0 + (i * sep): sep + (i * sep)])

            if (mod := model_len % sep) != 0:
                templist.append(model_names[-mod:])

            model_names = templist

        else:
            model_names = [model_names]

    return model_names


def get_speakers(model_name: str, *, sep: Optional[int] = None) -> Union[list[str], list[list[str]]]:
    modelfolder = ModelFolder(model_name)

    speaker_list = modelfolder.speakers

    # sepに値が入っていた場合model_namesをsepの値で分割したリストを返す
    if sep is not None:
        if sep <= 0:
            raise ValueError("'sep' value must be at least 1.")

        speaker_len = len(speaker_list)
        if speaker_len > sep:
            templist = []
            for i in range(speaker_len // sep):
                templist.append(speaker_list[0 + (i * sep): sep + (i * sep)])

            if (mod := speaker_len % sep) != 0:
                templist.append(speaker_list[-mod:])

            speaker_list = templist

        else:
            speaker_list = [speaker_list]

    return speaker_list


if __name__ == "__main__":
    s = get_speakers("RinneElu_TTSfree", sep=3)
    print(s)
