from socket import socket, AF_INET, SOCK_STREAM
import json
import sys
import time
from common.var import  DEF_SRV_ADDRESS, DEF_SRV_PORT, RESPONSE_CODE_ERROR, RESPONSE_CODE_SUCCESSFUL, LOGGING_ON
from common.utils import send_message, get_message
import logging
import log.conf_client_log

LOG = logging.getLogger('client')


def create_message() -> dict:
    message= {
        'action': 'presence',
        'time': time.time(),
        'user': {'account_name': 'Guest'}
    }
    LOG.debug(f'Сообщение "presence" создано') if LOGGING_ON else pass
    return message


def process_answer(message: dict) -> int:
    LOG.debug(f'Разбор сообщения от сервера: "{message}"') if LOGGING_ON else pass
    if 'response' in message:
        if message['response'] == RESPONSE_CODE_SUCCESSFUL:
            return RESPONSE_CODE_SUCCESSFUL
        return RESPONSE_CODE_ERROR
    raise ValueError


def main():
    LOG.debug(f'заапущен клиент ') if LOGGING_ON else pass
    srv_port = DEF_SRV_PORT
    srv_address = DEF_SRV_ADDRESS
    if len(sys.argv) == 2:
        srv_address = sys.argv[1]
    elif len(sys.argv) == 3:
        srv_address = sys.argv[1]
        try:
            srv_port = int(sys.argv[2])
            if srv_port < 1024 or srv_port > 65535:
                LOG.critical(f'Неверно указан порт : {srv_port}.'
                    f'Диапазон допустимых портов от 1024 до 65535') if LOGGING_ON else pass
                raise ValueError
        except ValueError:
            pass

    try:
        LOG.debug(f'Начинается попытка подключиться к серверу {srv_address}:{srv_port}, '
                     f'конечный компьютер отверг запрос на подключение.') if LOGGING_ON else pass
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((srv_address, srv_port))
        message_to = create_message()
        send_message(sock,message_to)
        answer = process_answer(get_message(sock))
        LOG.info(f'Принят ответ от сервера {answer}') if LOGGING_ON else pass
        print(answer)
    except (ValueError, json.JSONDecodeError):
            LOG.error('Не удалось декодировать сообщение сервера') if LOGGING_ON else pass
    except ConnectionRefusedError:
        LOG.critical(f'Не удалось подключиться к серверу {srv_address}:{srv_port}, '
                               f'конечный компьютер отверг запрос на подключение.') if LOGGING_ON else pass


if __name__ == '__main__':

    main()