import subprocess


lst_process = []

while True:
    key_action = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, '
                   'x - закрыть все окна: ')

    if key_action == 'q':
        break
    elif key_action == 's':
        lst_process.append(subprocess.Popen('python server.py',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        lst_process.append(subprocess.Popen('python client.py -n test1',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        lst_process.append(subprocess.Popen('python client.py -n test2',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        lst_process.append(subprocess.Popen('python client.py -n test3',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        lst_process.append(subprocess.Popen('python client.py -n test4',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        lst_process.append(subprocess.Popen('python client.py -n test5',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))

    elif key_action == 'x':
        while lst_process:
            killed_proc = lst_process.pop()
            killed_proc.kill()
