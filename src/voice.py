import requests
import json
import re

import data as f_data

url = f_data.read()["settings"]["url"]
port = f_data.read()["settings"]["port"]
default_model = f_data.read()["settings"]["default_model"]


def create_voice(mscontent, user_id):

    if type(user_id) == int:
        user_id = str(user_id)

    if user_id is None:
        user_data = None
    else:
        user_data = f_data.read_userdata(user_id)

    if user_data is not None:
        model_id = user_data["model_id"]
        speaker_id = user_data["speaker_id"]
        sdp_ratio = user_data["sdp_ratio"]
        noise = user_data["noise"]
        noisew = user_data["noisew"]
        length = user_data["length"]
        split_interval = user_data["split_interval"]
        assist_text = user_data["assist_text"]
        assist_text_weight = user_data["assist_text_weight"]
        style = user_data["style"]
        style_weight = user_data["style_weight"]
    else:
        model_id = default_model
        speaker_id = "0"
        sdp_ratio = "0.2"
        noise = "0.6"
        noisew = "0.8"
        length = "1"
        split_interval = "0.5"
        assist_text = ""
        assist_text_weight = "1"
        style = "Neutral"
        style_weight = "5"


    response_text = f"http://{url}:{port}/voice?text={mscontent}&encoding=utf-8&model_id={model_id}&speaker_id={speaker_id}&sdp_ratio={sdp_ratio}&noise={noise}&noisew={noisew}&length={length}&language=JP&auto_split=true&split_interval={split_interval}&assist_text_weight={assist_text_weight}&style={style}&style_weight={style_weight}"

    response = requests.get(response_text)

    wav = response.content

    path = "mscontent.wav"

    with open(path, "wb") as wr:
        wr.write(wav)

    return path

def get_model():
    response = requests.get(f"http://{url}:{port}/models/info")
    model_data = json.loads(response.content)

    print_text = ""
    print_dict = {}

    for i in range(len(model_data)):

        model_names = model_data[str(i)]["id2spk"]

        for i2 in range(len(model_names)):
            if i2 == 0:
                l = model_names[str(i2)]
            else:
                l = l + ", " + model_names[str(i2)]

        if i == 0:
            print_text = f"{str(i)}: {l}"
            print_dict[str(i)] = l
        else:
            print_text = f"{print_text}\n{str(i)}: {l}"
            print_dict[str(i)] = l



    return [print_dict, print_text]

def get_status():
    response = requests.get(f"http://{url}:{port}/status")
    status = json.loads(response.content)
    return status