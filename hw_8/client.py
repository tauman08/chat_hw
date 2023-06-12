from socket import socket, AF_INET, SOCK_STREAM
import json
import sys
import time
from common.var import  DEF_SRV_ADDRESS, DEF_SRV_PORT, RESPONSE_CODE_ERROR, RESPONSE_CODE_SUCCESSFUL, LOGGING_ON
from common.utils import send_message, get_message
import logging
import log.conf_client_log
from getpass import getpass
from logger import log
import argparse
from errors import ReqFieldMissingError, ServerError

LOG = logging.getLogger('client')

@log(LOG)
def arg_parser():
    """Создаём парсер аргументов коммандной строки
    и читаем параметры, возвращаем 3 параметра
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('address', default=DEF_SRV_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEF_SRV_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    address_port = parser.parse_args(sys.argv[1:])
    srv_addr = address_port.address
    srv_port = address_port.port
    client_mode = address_port.mode

    # проверим подходящий номер порта
    if not 1023 < srv_port < 65536:
        LOG.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {srv_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    # Проверим допустим ли выбранный режим работы клиента
    if client_mode not in ('listen', 'send'):
        LOG.critical(f'Указан недопустимый режим работы {client_mode}, '
                        f'допустимые режимы: listen , send')
        sys.exit(1)

    return srv_addr, srv_port, client_mode

@log(LOG)
def create_message_presence() -> dict:
    message= {
        'action': 'presence',
        'time': time.time(),
        'user': {'account_name': 'Guest'}
    }
    LOG.debug(f'Сообщение "presence" создано') if LOGGING_ON else getpass

    return message

@log(LOG)
def create_message(sock, account_name='Guest'):
    message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        sock.close()
        LOG.info('Завершение работы по команде пользователя.') if LOGGING_ON else getpass
        sys.exit(0)
    message_dict = {
        'action': 'message',
        'time': time.time(),
        'account_name': account_name,
        'message_txt': message
    }
    LOG.debug(f'Сформирован словарь сообщения: {message_dict}') if LOGGING_ON else getpass
    return message_dict


@log(LOG)
def process_answer(message: dict) -> int:
    LOG.debug(f'Разбор сообщения от сервера: "{message}"') if LOGGING_ON else getpass
    if 'response' in message:
        if message['response'] == RESPONSE_CODE_SUCCESSFUL:
            return RESPONSE_CODE_SUCCESSFUL
        elif message['response'] == RESPONSE_CODE_ERROR:
            raise ServerError(f'400 : {message["error"]}')
    raise ReqFieldMissingError('response')

@log(LOG)
def message_from_server(message):

    if 'action' in message and message['action'] == 'message' and \
            'sender' in message and 'message_txt' in message:
        print(f'Получено сообщение от пользователя '
              f'{message["sender"]}:\n{message["message_txt"]}')
        LOG.info(f'Получено сообщение от пользователя '
                    f'{message["sender"]}:\n{message["message_txt"]}') if LOGGING_ON else getpass
    else:
        LOG.error(f'Получено некорректное сообщение с сервера: {message}') if LOGGING_ON else getpass


def main():
    srv_address, srv_port, client_mode = arg_parser()
    LOG.debug(f'заапущен клиент ') if LOGGING_ON else getpass

    try:
        LOG.debug(f'Начинается попытка подключиться к серверу {srv_address}:{srv_port}, '
                     f'конечный компьютер отверг запрос на подключение.') if LOGGING_ON else getpass
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((srv_address, srv_port))
        message_presence = create_message_presence()
        send_message(sock,message_presence)
        answer = process_answer(get_message(sock))
        LOG.info(f'Установлено соединение с сервером. Принят ответ от сервера {answer}') if LOGGING_ON else getpass
        print('Установлено соединение с сервером')
    except (ValueError, json.JSONDecodeError):
            LOG.error('Не удалось декодировать сообщение сервера') if LOGGING_ON else getpass
    except ServerError as error:
        LOG.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        LOG.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        LOG.critical(f'Не удалось подключиться к серверу {srv_address}:{srv_port}, '
                               f'конечный компьютер отверг запрос на подключение.') if LOGGING_ON else getpass
        sys.exit(1)
    else:

        while True:
            if client_mode == 'send':
                try:
                    send_message(sock, create_message(sock))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOG.error(f'Соединение с сервером {srv_address} было потеряно.')
                    sys.exit(1)

            if client_mode == 'listen':
                try:
                    message_from_server(get_message(sock))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOG.error(f'Соединение с сервером {srv_address} было потеряно.')
                    sys.exit(1)



if __name__ == '__main__':

    main()