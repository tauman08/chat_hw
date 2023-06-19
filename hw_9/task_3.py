from ipaddress import ip_address
from task_1 import host_ping
from tabulate import tabulate


def host_range_ping_tab(ipv4:str, count_addr: int):
    last_oct = int(ipv4.split('.')[3])
    if (last_oct + count_addr) > 254:
        print(f'Меняем только последний октет. Максимальное кол-во хостов: {254-last_oct}')
        raise ValueError(f'Неверно задано количество хостов.')
    lst_host = [str(ip_address(ipv4)+ind) for ind in range(count_addr)]
    lst_dict_res = host_ping(lst_host, printing=False)
    print(tabulate(lst_dict_res,headers='keys'))


if __name__== "__main__":

    host_range_ping_tab('192.168.0.1',30)
