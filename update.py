import os
import shutil
import json
import time

deletelist = os.listdir("./")

for i in deletelist:
    if not i in ["data.json","update (need git).bat","update.py","Discord-ReadTextBot-for-Style-Bert-VITS2-API",".git"]:
        if os.path.isfile(i):
            os.remove(i)
        if os.path.isdir(i):
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

for i in oldjson["settings"].keys():
    newjson["settings"][i] = oldjson["settings"][i]

for i in ["user_data", "server_data"]:
    if i in oldjson:
        newjson[i] = oldjson[i]

with open('data.json', 'w') as f:
    json.dump(newjson, f, indent=4)

for i in ["data_old.json","update_old.py","update_old.bat"]:
    if os.path.exists(i):
        os.remove(i)

print("Update completed successfully!")

time.sleep(5)