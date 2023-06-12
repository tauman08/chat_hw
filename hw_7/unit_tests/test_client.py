from unittest import TestCase, main
from client import create_message, process_answer
from common.var import RESPONSE_CODE_SUCCESSFUL, RESPONSE_CODE_ERROR


class TestClient(TestCase):

    def test_create_message(self):
        test_dict = create_message()
        test_dict['time'] = 1
        self.assertEqual(test_dict,
            {'action': 'presence', 'time': 1, 'user': {'account_name': 'Guest'}})

    def test_process_answer_no_response(self):
        self.assertEqual(process_answer({}),ValueError)

    def test_process_answer_response_incorrect(self):
        self.assertEqual(process_answer({'response':RESPONSE_CODE_ERROR}),RESPONSE_CODE_ERROR)

    def test_process_answer_ok(self):
        self.assertEqual(process_answer({'response':RESPONSE_CODE_SUCCESSFUL}),RESPONSE_CODE_SUCCESSFUL)


if __name__ == '__main__':
    main()