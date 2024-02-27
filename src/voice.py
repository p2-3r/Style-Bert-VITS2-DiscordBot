import json
import re
import os

import aiohttp

import data as f_data

url = f_data.read()["settings"]["url"]
port = f_data.read()["settings"]["port"]
default_model = f_data.read()["settings"]["default_model"]


async def create_voice(mscontent: str, user_id: int, server_id: int):

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

    async with aiohttp.ClientSession() as session:
        async with session.get(response_text) as response:
            wav = await response.content.read()

            path = f"./temp/temp_{server_id}.wav"

            try:
                with open(path, "wb") as wr:
                    wr.write(wav)
            except FileNotFoundError:
                os.makedirs("./temp/", exist_ok=True)
                with open(path, "wb") as wr:
                    wr.write(wav)

            return path

async def get_model():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{url}:{port}/models/info") as response:
            model_data = await response.json()

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

async def get_speaker(model_id: int) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{url}:{port}/models/info") as response:
            model_data = await response.json()
            return model_data[str(model_id)]["id2spk"]

async def get_status():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{url}:{port}/status") as response:
            status = await response.json()
            return status

