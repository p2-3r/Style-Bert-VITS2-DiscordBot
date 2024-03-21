from pathlib import Path
from glob import glob
import re

DEBUG = False

if not DEBUG:
    from style_bert_vits2.tts_model import TTSModel
    from style_bert_vits2.nlp import bert_models
    from style_bert_vits2.constants import Languages
    from style_bert_vits2.nlp.japanese.g2p_utils import g2kata_tone
    from style_bert_vits2.nlp.japanese.normalizer import normalize_text

    bert_models.load_model(
        Languages.JP, "ku-nlp/deberta-v2-large-japanese-char-wwm")
    bert_models.load_tokenizer(
        Languages.JP, "ku-nlp/deberta-v2-large-japanese-char-wwm")

    class Load():
        @classmethod
        def model(cls, *, model_file: Path, config_file: Path, style_file: Path, device: str = "cuda"):
            model = TTSModel(
                model_path=model_file,
                config_path=config_file,
                style_vec_path=style_file,
                device=device
            )
            return model

    class Model_Get():

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


class ModelFolder():
    def __init__(self, model_name: str) -> None:
        g = glob(str(assets_root) + "/**/")
        folder_names = [Path(i) for i in g]

        model_names = []
        for i in folder_names:
            config_json = (i/"config.json").exists()
            vectors_npy = (i/"style_vectors.npy").exists()
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
        re_safetensors = [i for i in self.safetensors if re.match(
            ".+_e[0-9]+_s[0-9]+.safetensors", i.name)]

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
                device="cuda"
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
                device="cuda"
            )

            return Model_Get.styles(model)
        return ['Neutral', 'Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise']


def get_modelfolders() -> list[str]:
    g = glob(str(assets_root) + "/**/")
    folder_names = [Path(i) for i in g]

    model_names = []
    for i in folder_names:
        config_json = (i/"config.json").exists()
        vectors_npy = (i/"style_vectors.npy").exists()
        model_safetensors = len(list(i.glob("*.safetensors")))

        if all([config_json, vectors_npy, model_safetensors]):
            model_names.append(i.name)

    return model_names


if __name__ == "__main__":
    # 使用例
    m = ModelFolder("RinneElu_TTSfree")
    print(m.styles, m.json, m.npy, m.safetensors, m.latest_safetensors, sep="\n")
