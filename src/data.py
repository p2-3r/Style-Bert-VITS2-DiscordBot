import json
import re

def read():
    f = open("data.json" , "r")
    data = json.load(f)
    return data

def write(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

def read_userdata(user_id):

    if type(user_id) == int:
        user_id = str(user_id)
    
    f = open("data.json" , "r")
    data = json.load(f)
    if user_id in data["user_data"]:
        return data["user_data"][user_id]
    else:
        return None

def create_userdata(user_id):
    f = open("data.json" , "r")
    data = json.load(f)

    data["user_data"][user_id] = {"model_id": "0",
                                  "speaker_id": "0",
                                  "sdp_ratio": "0.2",
                                  "noise": "0.6",
                                  "noisew": "0.8",
                                  "length": "1",
                                  "split_interval": "0.5",
                                  "assist_text": "",
                                  "assist_text_weight": "1",
                                  "style": "Neutral",
                                  "style_weight": "5"}
    
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    
def write_userdata(user_id, user_data):

    if type(user_id) == int:
        user_id = str(user_id)

    f = open("data.json" , "r")
    data = json.load(f)

    if user_id in data["user_data"]:
        data["user_data"][user_id] = user_data

    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

def fullnum2halfnum(input):

    fullnum = "０１２３４５６７８９．"
    halfnum = "0123456789."

    map = str.maketrans(fullnum, halfnum) 
    l = input.translate(map)

    return l

