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
from errors import ReqFieldMissingError, ServerError, IncorrectDataRecivedError
import threading

LOG = logging.getLogger('client')

@log(LOG)
def arg_parser():
    """Создаём парсер аргументов коммандной строки
    и читаем параметры, возвращаем 3 параметра
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('address', default=DEF_SRV_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEF_SRV_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default='', nargs='?')
    address_port = parser.parse_args(sys.argv[1:])
    srv_addr = address_port.address
    srv_port = address_port.port
    client_name = address_port.name

    # проверим подходящий номер порта
    if not 1023 < srv_port < 65536:
        LOG.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {srv_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.') if LOGGING_ON else getpass
        sys.exit(1)

    # Проверим допустим ли выбранный режим работы клиента
    if client_name != '':
        LOG.critical('Не задано имя клиента ') if LOGGING_ON else getpass
        sys.exit(1)

    return srv_addr, srv_port, client_name

@log(LOG)
def create_message_presence(account_name) -> dict:
    message= {
        'action': 'presence',
        'time': time.time(),
        'user': {'account_name': account_name}
    }
    LOG.debug(f'Сообщение "presence" создано') if LOGGING_ON else getpass

    return message

@log(LOG)
def create_message(sock, account_name):
    message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        sock.close()
        LOG.info('Завершение работы по команде пользователя.') if LOGGING_ON else getpass
        sys.exit(0)
    to_account = input('Введите аккаунт получателя сообщения: ')
    message = input('Введите сообщение: ')
    message_dict = {
        'action': 'message',
        'sender': account_name,
        'destination': to_account,
        'time': time.time(),
        'message_txt': message
    }
    LOG.debug(f'Сформирован словарь сообщения: {message_dict}') if LOGGING_ON else getpass
    try:
        send_message(sock,message_dict)
        LOG.info(f'Отправлено сообщение пользователю {message_dict}') if LOGGING_ON else getpass
    except:
        LOG.critical('Потеряно соединение с сервером.')
        sys.exit(1)

@log(LOG)
def input_message(sock, my_username):
    while True:
        try:
            message = get_message(sock)
            if 'action' in message and message['action'] == 'message' and \
                'sender' in message and 'destination' in message \
                and 'message_txt' in message and message['destination'] == my_username:
                print(f'Получено сообщение от пользователя: {message["sender"]}')
                LOG.info(f'Получено сообщение от пользователя: {message["sender"]}') if LOGGING_ON else getpass
            else:
                LOG.info(f'Получено некорректное сообщение с сервера: {message}') if LOGGING_ON else getpass
        except IncorrectDataRecivedError:
            LOG.error(f'Не удалось декодировать полученное сообщение.')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            LOG.critical(f'Потеряно соединение с сервером.') if LOGGING_ON else getpass
            break

def help():
    print('Поддерживаемые команды:')
    print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')


def create_exit_message(account_name):
    return {
        'action': 'exit',
        'time': time.time(),
        'account_name': account_name
    }

@log(LOG)
def user_working(sock, username):
    help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message(sock, username)
        elif command == 'help':
            help()
        elif command == 'exit':
            send_message(sock, create_exit_message(username))
            print('Завершение соединения.')
            LOG.info('Завершение работы по команде пользователя.') if LOGGING_ON else getpass
            time.sleep(0.5)
            break
        else:
            print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')

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
    srv_address, srv_port, client_name = arg_parser()

    if not client_name:
        client_name = input('Введите имя пользователя: ')

    LOG.debug(f'запущен клиент {client_name} ') if LOGGING_ON else getpass

    try:
        LOG.debug(f'Начинается попытка подключиться к серверу {srv_address}:{srv_port}, '
                     f'конечный компьютер отверг запрос на подключение.') if LOGGING_ON else getpass
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((srv_address, srv_port))
        message_presence = create_message_presence(client_name)
        send_message(sock, message_presence)
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
        postman = threading.Thread(target=message_from_server, args=(socket,client_name))
        postman.daemon = True
        postman.start()

        user_work = threading.Thread(target=user_working, args=(socket,client_name))
        user_work.daemon = True
        user_work.start()
        while True:
            time.sleep(1)
            if not postman.isAlive() or not user_work.isAlive():
                break


if __name__ == '__main__':

    main()