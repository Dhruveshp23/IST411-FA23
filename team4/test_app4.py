# Project: Project Diamond 
# Purpose Details: Unit tests for App4 of Project Diamond  
# Course: IST 411 
# Author: Team 4 
# Date Developed: 11/26/2023 
# Last Date Changed: 11/29/2023 
# Rev: 1

import unittest
from unittest.mock import patch
from io import StringIO
import requests
from app4 import App4Receiver, log_to_app5

class TestApp4Receiver(unittest.TestCase):
    """
    Test cases for the App4Receiver class.
    """

    def setUp(self):
        """
        Set up the test environment by initializing the App4Receiver instance.
        """
        self.receiver = App4Receiver()

    @patch('app4.log_to_app5')
    def test_receive_python_object_success(self, mock_log_to_app5):
        """
        Test the successful reception of a Python object.

        It checks if the receive_python_object method correctly processes
        the Python object and logs the success message.
        """
        python_object = {'key': 'value'}
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.receiver.receive_python_object(python_object)

        mock_log_to_app5.assert_called_once_with('receive_python_object_success_from_app4')

        expected_output = "Received Python object:\n{\n  \"key\": \"value\"\n}\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('app4.log_to_app5')
    def test_failed_to_process_python_object(self, mock_log_to_app5):
        """
        Test the scenario where an error occurs during Python object processing.

        It checks if the receive_python_object method handles exceptions
        correctly and logs the failure message.
        """
        python_object = {'key': 'value'}
        with patch('json.dumps', side_effect=Exception('Test exception')):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.receiver.receive_python_object(python_object)

        mock_log_to_app5.assert_called_once_with('failed_to_process_python_object')

        expected_output = "An error occurred during Python object processing: Test exception\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

class TestLogToApp5(unittest.TestCase):
    """
    Test cases for the log_to_app5 function.
    """

    @patch('app4.requests.post')
    @patch('app4.logging.info')
    def test_log_to_app5_success(self, mock_info, mock_post):
        """
        Test successful logging to App5.

        It checks if log_to_app5 function makes a successful POST request
        and logs the success message.
        """
        log_to_app5('test_action')

        mock_post.assert_called_once_with(
            'http://localhost:5000/log/test_action',
            json={},
            headers={'Content-Type': 'application/json'}
        )

        expected_log_message = 'PASS: Logged action into App5: test_action'
        actual_log_message = mock_info.call_args[0][0]
        self.assertIn(expected_log_message, actual_log_message)

    @patch('app4.requests.post', side_effect=requests.exceptions.RequestException('Test exception'))
    @patch('app4.logging.error')
    def test_log_to_app5_failure(self, mock_error, mock_post):
        """
        Test failure in logging to App5.

        It checks if log_to_app5 function handles the failure scenario
        and logs the error message.
        """
        log_to_app5('test_action')

        mock_post.assert_called_once_with(
            'http://localhost:5000/log/test_action',
            json={},
            headers={'Content-Type': 'application/json'}
        )

        expected_log_message = 'Failed to log action into App5: Test exception'
        actual_log_message = mock_error.call_args[0][0]
        self.assertIn(expected_log_message, actual_log_message)

if __name__ == '__main__':
    unittest.main()
