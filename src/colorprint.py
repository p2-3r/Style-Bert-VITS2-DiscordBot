import datetime

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

    now = datetime.datetime.now()

    def time(self):
        l = f'{self.now.hour}:{self.now.minute}:{self.now.second}'
        j = color.print(l, color.GREEN)
        return j

    def info(self, content):
        print(f"{color.print('INFO', color.BLUE)}|{Printinfo().time()}|{content}")

    def error(self, content):
        print(f"{color.print('ERROR', color.RED)}|{Printinfo().time()}|{content}")

    def complete(self, content):
        print(f"{color.print('COMPLETE', color.YELLOW)}|{Printinfo().time()}|{content}")

printinfo = Printinfo()