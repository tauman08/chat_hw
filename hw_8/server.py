import logging
import time
from getpass import getpass
from socket import socket, AF_INET, SOCK_STREAM
import json
import sys
from common.var import DEF_SRV_PORT, DEF_SRV_ADDRESS, MAX_CONNECTIONS, RESPONSE_CODE_SUCCESSFUL, RESPONSE_CODE_ERROR, LOGGING_ON
from common.utils import get_message, send_message
import log.conf_srv_log
from logger import log
from select import select
import argparse


LOG = logging.getLogger('server')

@log(LOG)
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a',default=DEF_SRV_ADDRESS,nargs='?')
    parser.add_argument('-p',default=DEF_SRV_PORT,type=int,nargs='?')
    address_port = parser.parse_args()
    if not 1023 < address_port.p < 65536:
        LOG.critical(
            f'Попытка запуска сервера с указанием неподходящего порта '
            f'{address_port.p}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)

    return address_port.a, address_port.p



@log(LOG)
def process_message(message: dict, lst_messages: list, client: socket):

    LOG.debug(f'Обработка сообщения от клиента: {message}') if LOGGING_ON else getpass

    if 'action' in message and message['action'] == 'presence' \
            and 'time' in message and 'user' in message and message['user']['account_name'] != '':

        name_user = message['account_name']
        exist_lst = [msg[0] for msg in lst_messages if msg[0] == name_user]
        if len(exist_lst) == 0:
            send_message(client, {'response': RESPONSE_CODE_SUCCESSFUL})
        else:
            send_message(client, {'response': RESPONSE_CODE_ERROR,
                                  'error': 'Уже существует пользователь с таким именем'})

        return
    elif 'action' in message and message['action'] == 'message' and \
            'time' in message and 'message_txt' in message:
        lst_messages.append((message['account_name'], message['message_txt']))
        return
    else:
        send_message(client, {
            'response': RESPONSE_CODE_ERROR,
            'error': 'Bad Request'
        })
        return


def main():

    srv_address,srv_port = arg_parser()
    LOG.info(f'Запущен сервер по адресу {srv_address} порт {srv_port}') if LOGGING_ON else getpass

    listen_socket = socket(AF_INET, SOCK_STREAM)
    listen_socket.bind((srv_address,srv_port))
    listen_socket.settimeout(0.2)
    listen_socket.listen(MAX_CONNECTIONS)

    lst_clients = []
    lst_messages = []
    while True:
        try:
            client, client_addr = listen_socket.accept()
        except OSError:
            pass
        else:
            LOG.info(f'Установлено соединение с клиентом {client_addr}')
            lst_clients.append(client)
        recv_lst = []
        send_lst = []
        err_lst = []
        try:
            if lst_clients:
                recv_lst, send_lst, err_lst = select(lst_clients, lst_clients, [], 0)
        except OSError:
            pass

        if recv_lst:
            for client_message in recv_lst:
                try:
                    process_message(get_message(client_message),lst_messages,client_message)
                except:
                    LOG.info(f'Клиент {client_message.getpeername()} отключился от сервера')
                    lst_clients.remove(client_message)

        if lst_messages and send_lst:
            message = {
                'action':'message',
                'sender':lst_messages[0][0],
                'time':time.time(),
                'message_txt':lst_messages[0][1]
            }
            del lst_messages[0]
            for client in send_lst:
                try:
                    send_message(client, message)
                except:
                    LOG.info(f'Клиент {client.getpeername()} отключился от сервера.')
                    lst_clients.remove(client)


if __name__ == '__main__':
    main()