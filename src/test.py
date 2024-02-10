import re 
  
def Find(string): 
    # findall() 正規表現に一致する文字列を検索する
    url = re.findall('https?://(?:[-A-Za-z0-9_.]|(?:%[\da-fA-F]{2}))+', string)
    return url 

string = 'Ceodata のホームページは：https://www.ceodata.comです，Google のホームページは：https://www.google.comです'

j = string
for i in Find(j):
    j = j.replace(i, '(url)')
print(j)

#print("Urls: ", Find(string))