import logging
from socket import socket, AF_INET, SOCK_STREAM
import json
import sys
from common.var import DEF_SRV_PORT, DEF_SRV_ADDRESS, MAX_CONNECTIONS, RESPONSE_CODE_SUCCESSFUL, RESPONSE_CODE_ERROR, LOGGING_ON
from common.utils import get_message, send_message
import log.conf_srv_log


LOG = logging.getLogger('server')


def process_message(message: dict):

    LOG.debug(f'Обработка сообщения от клиента: {message}') if LOGGING_ON else pass
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
        if srv_port < 1024 or srv_port > 65535:

            raise ValueError
    except IndexError:
        LOG.critical((f'неверно указана командная строка')) if LOGGING_ON else pass
        sys.exit(2)
    except ValueError:
        LOG.critical((f'Запуск сервера с неверным портом {srv_port}. ДОпустимы номера портов с 1024 по 65535')) if LOGGING_ON else pass

        sys.exit(2)
    try:
        if '-a' in sys.argv:
            srv_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            srv_address = DEF_SRV_ADDRESS
    except IndexError:
        LOG.critical((f'Не указан адрес сервера')) if LOGGING_ON else pass
        sys.exit(2)
    LOG.info(f'Запущен сервер по адресу {srv_address} порт {srv_port}') if LOGGING_ON else pass
    listen_socket = socket(AF_INET, SOCK_STREAM)
    listen_socket.bind((srv_address,srv_port))

    listen_socket.listen(MAX_CONNECTIONS)

    try:
        while True:
            client, client_address = listen_socket.accept()
            try:
                message = get_message(client)
                LOG.debug(f'Получено сообщение: {message}') if LOGGING_ON else pass
                response = process_message(message)
                LOG.debug(f'Сформирован ответ клиенту: {response}') if LOGGING_ON else pass
                send_message(client, response)
                LOG.debug(f'Закрытие клиентского {client_address} соединения') if LOGGING_ON else pass
                client.close()
            except (ValueError, json.JSONDecodeError):
                LOG.critical(f'От клиента {client_address} пришли некорректные данные') if LOGGING_ON else pass
                client.close()
    finally:
        listen_socket.close()


if __name__ == '__main__':
    main()