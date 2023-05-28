from socket import socket, AF_INET, SOCK_STREAM
import json
import sys
from common.var import DEF_SRV_PORT, DEF_SRV_ADDRESS, MAX_CONNECTIONS, RESPONSE_CODE_SUCCESSFUL, RESPONSE_CODE_ERROR
from common.utils import get_message, send_message


def process_message(message: dict):

    if 'action' in message and message[action] == 'presence' \
            and 'time' in message and 'user' in message and message['user']['account_name'] == 'Guest':
        return {'response': RESPONSE_CODE_SUCCESSFUL}
    return {'response': RESPONSE_CODE_ERROR, 'error': 'Bad request'}


def main():
    try:
        if '-p' in sys.argv:
            srv_port = int(sys.argv[sys.argv.index('-p')+1])
        else:
            srv_port = DEF_SRV_PORT
        if srv_port < 1024 or srv_port > 65535
            raise ValueError
    except IndexError:
        print('Не указан номер порта.')
        sys.exit(2)
    except ValueError:
        print('неверно указан номер порта')
        sys.exit(2)
    try:
        if '-a' in sys.argv:
            srv_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            srv_address = DEF_SRV_ADDRESS
    except IndexError:
        print('Не указан адрес.')
        sys.exit(2)

    listen_socket = socket(AF_INET, SOCK_STREAM)
    listen_socket.bind((srv_address,srv_port))

    listen_socket.listen(MAX_CONNECTIONS)

    try:
        while True:
            client, client_address = listen_socket.accept()
            try:
                message = get_message(client)
                print(message)
                response = process_message(message)
                send_message(client, response)
                client.close()
            except (ValueError, json.JSONDecodeError):
                print('Некорректное сообщение.')
                client.close()
    finally:
        listen_socket.close()


if __name__ == '__main__':
    main()