import json
import re

def read():
    with  open("data.json" , "r") as f:
        data = json.load(f)
    return data

def write(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

def read_userdata(user_id):

    if type(user_id) == int:
        user_id = str(user_id)
    
    data = read()

    if user_id in data["user_data"]:
        return data["user_data"][user_id]
    else:
        return None

def create_userdata(user_id):
    
    data = read()

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
    
    write(data)
    
def write_userdata(user_id, user_data):

    if type(user_id) == int:
        user_id = str(user_id)

    data = read()

    if user_id in data["user_data"]:
        data["user_data"][user_id] = user_data

    write(data)

def read_serverdata(server_id):
    data_json = read()

    if type(server_id) == int:
         server_id = str(server_id)

    try:
        servers_data = data_json["server_data"]
    except KeyError:
        data_json["server_data"] = {}
        write(data_json)

    servers_data_template = {"auto_join": False,
                             "auto_join_read_channel": None}
         
    try:
        current_server_data = servers_data[server_id]
    except KeyError:
        servers_data[server_id] = servers_data_template
        write(data_json)
        current_server_data = servers_data[server_id]

    t_l = False
    for i in servers_data_template.keys():
        try:
            j = current_server_data[i]
        except KeyError:
            current_server_data[i] = servers_data_template[i]
            if t_l == False:
                t_l = True

        if t_l == True:
            write(data_json)
    
    return current_server_data

def write_serverdata(server_id,server_data):

    if type(server_id) == int:
         server_id = str(server_id)

    data_json = read()
    data_json["server_data"][server_id] = server_data

    write(data_json)

def fullnum2halfnum(input):

    fullnum = "０１２３４５６７８９．"
    halfnum = "0123456789."

    map = str.maketrans(fullnum, halfnum) 
    l = input.translate(map)

    return l

