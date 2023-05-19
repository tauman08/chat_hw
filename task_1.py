#Задание 1
#1.
from typing import List

lst_string = ['разработка', 'сокет', 'декоратор']

for el in lst_string:
    print(f'строка "{el}" тип {type(el)}')
    str_utf = el.encode("utf-8")
    print(f'строка "{el}" в Unicode(utf-8): "{str_utf}" тип: "{type(str_utf)}"')
#2.

lst_str = ['class', 'function', 'method']
lst_utf: list[bytes] = [bytes(el,'utf-8') for el in lst_str]

for el in lst_utf:
    print(f'исходная строка "{lst_str[lst_utf.index(el)]}" байты  {el} тип "{type(el)}" длина {len(el)}')

#3.

lst_str = ['class', 'function', 'method']
lst_utf: list[bytes] = []

for el in lst_str:
    try:
        print(f'строка "{el}" в байтах: {bytes(el,"ascii")}')
    except UnicodeEncodeError:
        print(f'строку "{el}" невозможно записать в байтовом типе')

#4
lst_str = ['разработка', 'администрирование', 'protocol', 'standard']
lst_utf: list[bytes] = [el.encode('utf-8') for el in lst_str]

for el in lst_utf:
    print(f' исходная строка "{lst_str[lst_utf.index(el)]}" байты {el} раскодираванная "{el.decode("utf-8")}"')

#5
import subprocess
import chardet


def ping_web(args):
    ping = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in ping.stdout:
        print(f'Байты в исходной кодировке  {line}')
        result = chardet.detect(line)
        print(f'словарь с описанием кодировки : {result}')
        line = line.decode(result['encoding']).encode('utf-8')
        print(f'Снова байты в utf-8: {line} \n строка полученная из utf-8: {line.decode("utf-8")}')


args = ('ping', 'yandex.ru')
ping_web(args)
print('youtube.com')
args = ('ping', 'youtube.com')
ping_web(args)

#6
detect = chardet.detect
with open('text.txt','rb') as f:
    content_f = f.read()
    detected = detect(content_f)
    content_str =  content_f.decode(detected['encoding'])
with open('text.txt','w',encoding='utf-8') as f:
    f.write(content_str)

with open('text.txt',encoding='utf-8') as f:
    for line in f.read():
        print(line, end='')

#конец домашнего задания
