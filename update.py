import os
import shutil
import json
import time
import datetime

def now():
    return datetime.datetime.now()

class Color:

    RED = '[31m'
    BLUE = '\033[34m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    END = '\033[0m'

    def print(self, content, color):
        return color + content + self.END

color = Color()

class Printinfo:

    def time(self):
        l = f'{now().hour}:{now().minute}:{now().second}'
        j = color.print(l, color.GREEN)
        return j

    def info(self, content):
        print(f"{color.print('INFO', color.BLUE)}|{Printinfo().time()}|{content}")

    def error(self, content):
        print(f"{color.print('ERROR', color.RED)}|{Printinfo().time()}|{content}")

    def complete(self, content):
        print(f"{color.print('COMPLETE', color.YELLOW)}|{Printinfo().time()}|{content}")

printinfo = Printinfo()

def exist_and_delete(file_path):
    if os.path.exists(file_path):

        if os.path.isfile(file_path):
            os.remove(file_path)

        if os.path.isdir(file_path):
            shutil.rmtree(file_path)

def exist_and_rename(before,after):
    if os.path.exists(before):
        os.rename(before, after)

try:
    deletelist = os.listdir("./")

    printinfo.info("Deleting old files...")

    for i in deletelist:
        if not i in ["data.json","update (need git).bat","update.py","requirements.txt","venv","Discord-ReadTextBot-for-Style-Bert-VITS2-API",".git"]:
            exist_and_delete(i)

    rename_dict = {"data.json": "data_old.json",
                   "update (need git).bat": "update_old.bat",
                   "update.py": "update_old.py",
                   "requirements.txt": "requirements_old.txt"}

    for before, after in rename_dict.items():
        exist_and_rename(before, after)

    printinfo.info("Moving new files...")

    for i in os.listdir("./Discord-ReadTextBot-for-Style-Bert-VITS2-API"):
        join_path = "./Discord-ReadTextBot-for-Style-Bert-VITS2-API/" + i
        shutil.move(join_path,"./")

    exist_and_delete("Discord-ReadTextBot-for-Style-Bert-VITS2-API")

    if os.path.exists("data.json"):

        printinfo.info("Moving 'data.json'...")

        newjson = json.load(open('data.json', 'r', encoding="UTF-8"))
        oldjson = json.load(open('data_old.json', 'r', encoding="UTF-8"))

        for i in oldjson["settings"].keys():
            newjson["settings"][i] = oldjson["settings"][i]

        for i in ["user_data", "server_data"]:
            if i in oldjson:
                newjson[i] = oldjson[i]

        with open('data.json', 'w') as f:
            json.dump(newjson, f, indent=4)

    if os.path.exists("requirements_old.txt"):

        with open("requirements_old.txt", "r", encoding="cp932") as f:
            req_old = f.read()
        with open("requirements.txt", "r", encoding="cp932") as f:
            req_new = f.read()

        if not req_old == req_new:
            exist_and_delete("venv")
            printinfo.info("Deleted venv because there was a change in the using library.")
    else:
        printinfo.info("Deleted venv because there was no requirements.txt")
        exist_and_delete("venv")

    for i in ["data_old.json","update_old.py","update_old.bat","requirements_old.txt"]:
        exist_and_delete(i)

    printinfo.complete("Update completed successfully!")
    printinfo.info("This window will close automatically after 10 seconds.")
    time.sleep(10)

except Exception as e:
    printinfo.error(str(e))
    printinfo.error('An error occurred, please manually move "data.json"')
    time.sleep(60)
