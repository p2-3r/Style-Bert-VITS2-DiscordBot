import os
import shutil
import json

deletelist = ["run_botandAPI.bat","run_bot.bat","run_API.bat","requirements.txt","mscontent.wav","README.md","LICENSE"]
deletefolderlist = ["venv","src"]

for i in deletelist:
    if os.path.exists(i):
        os.remove(i)

for i in deletefolderlist:
    if os.path.exists(i):
        shutil.rmtree(i)
        
if os.path.exists("data.json"):
    os.rename("data.json", "data_old.json")
if os.path.exists("update (need git).bat"): 
    os.rename("update (need git).bat","update_old.bat")
if os.path.exists("update.py"): 
    os.rename("update.py","update_old.py")

move_file_list = os.listdir("./Discord-ReadTextBot-for-Style-Bert-VITS2-API")

for i in move_file_list:
    join_path = "./Discord-ReadTextBot-for-Style-Bert-VITS2-API/" + i
    shutil.move(join_path,"./")

shutil.rmtree("Discord-ReadTextBot-for-Style-Bert-VITS2-API")

newjson = json.load(open('data.json', 'r', encoding="UTF-8"))
oldjson = json.load(open('data_old.json', 'r', encoding="UTF-8"))

k_list = oldjson["settings"].keys()

for i in k_list:
    newjson["settings"][i] = oldjson["settings"][i]

newjson["user_data"] = oldjson["user_data"]

with open('data.json', 'w') as f:
    json.dump(newjson, f, indent=4)

for i in ["data_old.json","update_old.py","update_old.bat"]:
    if os.path.exists(i):
        os.remove(i)