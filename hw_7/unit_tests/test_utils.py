from unittest import TestCase, main
from common.utils import get_message, send_message
import json
from common.var import MAX_PACKAGE_LENGTH, ENCODING
from common.var import RESPONSE_CODE_SUCCESSFUL, RESPONSE_CODE_ERROR


class TestSocket:

    def __init__(self, message: dict):
        self.message = message
        self.encoded_message = None
        self.sent_message = None

    def recv(self,max_len):
        return json.dumps(self.message).encode(ENCODING)

    def send(self, message):
        pass


class TestClass(TestCase):
    message = {
        'action': 'presence',
        'time': 1,
        'user': {'account_name': 'Guest'}
    }
    recv_ok = {'response', RESPONSE_CODE_SUCCESSFUL}
    recv_error = {'response', RESPONSE_CODE_ERROR}

    def test_get_message(self):

        self.assertEqual(get_message(TestSocket(self.recv_ok)),self.recv_ok)
        self.assertEqual(get_message(TestSocket(self.recv_error)), self.recv_ok)

    def test_send_message(self):
        send_message(TestSocket(self.message),self.message)
        with self.assertRaises(Exception):
            send_message(TestSocket(self.message),'')


if __name__ == '__main__':
    main()