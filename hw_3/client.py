from socket import socket, AF_INET, SOCK_STREAM
import json
import sys
import time
from common.var import  DEF_SRV_ADDRESS, DEF_SRV_PORT, RESPONSE_CODE_ERROR, RESPONSE_CODE_SUCCESSFUL
from common.utils import send_message, get_message


def create_message() -> dict:
    message= {
        'action': 'presence',
        'time': time.time(),
        'user': {'account_name': 'Guest'}
    }
    return message


def process_answer(message: dict) -> int:
    if 'response' in message:
        if message['response'] == RESPONSE_CODE_SUCCESSFUL:
            return RESPONSE_CODE_SUCCESSFUL
        return RESPONSE_CODE_ERROR
    raise ValueError


def main():
    srv_port = DEF_SRV_PORT
    srv_address = DEF_SRV_ADDRESS
    if len(sys.argv) == 1:
        srv_address = sys.argv[1]
    elif len(sys.argv) == 2:
        srv_address = sys.argv[1]
        try:
            srv_port = int(sys.argv[2])
            if srv_port < 1024 or srv_port > 65535:
                raise ValueError
        except ValueError:
            print('Неверно указан порт. Диапазон допустимых портов от 1024 до 65535')

    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((srv_address, srv_port))
    message_to = create_message()
    send_message(sock,message_to)
    try:
        answer = process_answer(get_message(sock))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера')


if __name__ == '__main__':
    main()