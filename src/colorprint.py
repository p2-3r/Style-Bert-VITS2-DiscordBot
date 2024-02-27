import datetime

def now():
    return datetime.datetime.now()

class Color:

    RED = '\033[31m'
    BLUE = '\033[34m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    END = '\033[0m'

    @classmethod
    def print(self, content, color):
        return color + content + self.END

class Printinfo:

    @classmethod
    def time(self):
        l = f'{now().hour:02}:{now().minute:02}:{now().second:02}'
        j = Color.print(l, Color.GREEN)
        return j

    @classmethod
    def info(self, content):
        print(f"{Color.print('INFO', Color.BLUE)}|{self.time()}|{content}")

    @classmethod
    def error(self, content):
        print(f"{Color.print('ERROR', Color.RED)}|{self.time()}|{content}")

    @classmethod
    def complete(self, content):
        print(f"{Color.print('COMPLETE', Color.YELLOW)}|{self.time()}|{content}")