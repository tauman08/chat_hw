import subprocess
from ipaddress import ip_address
import chardet
import re
from getpass import getpass


def ip_for_domen(name_domen: str) -> str:
    args = ['ping', name_domen]
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    data = process.communicate()
    charset = chardet.detect(data[0])
    str_out = data[0].decode(charset['encoding'])

    match = re.search(r'\d+.\d+.\d+.\d+', str_out)

    if match == None:
         return ''
    else:
        str_ip = match.group(0)
        return str_ip


def host_ping(lst_address: list, printing=True) -> dict:
    result = []
    dict_result = {'Доступные узлы':'','Недоступные узлы':''}
    for addr in lst_address:
        try:
            address = ip_address(addr)
        except ValueError:
            ip = ip_for_domen(addr)
            if ip != '':
                address = ip_address(ip)
            else:
                raise ValueError(f'Неверное доменное имя: {addr}')
        process = subprocess.Popen(['ping', str(address)], shell=False, stdout=subprocess.PIPE)
        process.wait()
        if process.returncode == 0:
            result.append({'Доступные узлы': f"{str(address)}"})
            print(f'Узел {addr} доступен') if printing else getpass
        else:
            result.append({'Недоступные узлы': f"{str(address)}"})
            print(f'Узел {addr} недоступен') if printing else getpass
    return result

def main():
    lst = ['www.google.com', 'www.yandex.ru', 'www.mail.ru', '192.168.1.178']
    host_ping(lst)


if __name__ == '__main__':
    main()
