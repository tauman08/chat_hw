from unittest import TestCase, main
from server import process_message
import time


class TestSrv(TestCase):

    dict_error = {'response': 400, 'error': 'Bad request'}
    dict_successful = {'response': 200}

    def test_no_action(self):
        self.assertEqual(process_message(
            {'time': time.time(), 'user': {'account_name': 'Guest'}}), self.dict_error)

    def test_action_incorrect(self):
        self.assertEqual(process_message(
            {'action': 'error','time': time.time(),'user': {'account_name': 'Guest'}}),self.dict_error)

    def test_no_time(self):
        self.assertEqual(process_message(
            {'action': 'presence','user': {'account_name': 'Guest'}}),self.dict_error)

    def test_no_user(self):
        self.assertEqual(process_message(
            {'action': 'presence', 'time': time.time()}), self.dict_error)

    def test_no_account_name(self):
        self.assertEqual(process_message(
            {'action': 'presence', 'time': time.time(), 'user': {}}), self.dict_error)

    def test_account_name_incorrect(self):
        self.assertEqual(process_message(
            {'action': 'presence', 'time': time.time(), 'user': {'account_name': 'admin'}}), self.dict_error)

    def test_ok(self):
        self.assertEqual(process_message(
            {'action': 'presence', 'time': time.time(), 'user': {'account_name': 'Guest'}}), self.dict_successful)


if __name__ == '__main__':
    main()