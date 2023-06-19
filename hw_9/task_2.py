from task_1 import host_ping


def host_range_ping(ipv4:str, range_ip: tuple):
    ind = ipv4.rfind('.')
    if ind == -1:
        print('Неверный формат адреса.')
        return
    if range_ip[1] > 254:
        print(f"Можем менять только последний октет")
        return
    start_ip = ipv4[:ind]
    lst_host = ['.'.join([start_ip, str(last_oct)])  for last_oct in range(range_ip[0], range_ip[1]+1)]
    return host_ping(lst_host)


if __name__== "__main__":
    host_range_ping('192.168.0.1',(5,10))



