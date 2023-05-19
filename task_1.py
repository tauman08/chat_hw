#Задание 1



#1.
from typing import List
lst_str = ['разработка', 'сокет', 'декоратор']
for el in lst_str:
    print(f'строка "{el}" тип {type(el)}')
    str_utf = el.encode("utf-8")
    print(f'строка "{el}" в Unicode(utf-8): "{str_utf}" тип: "{type(str_utf)}"')
