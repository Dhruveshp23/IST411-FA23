# Project: Project Diamond 
# Purpose Details: Unit tests for App 3 of Project Diamond 
# Course: IST 411 
# Author: Team 4 
# Date Developed: 10/29/2023 
# Last Date Changed: 11/29/2023 
# Rev: 1 

"""
test_app3.py - Unit tests for the app3 module.

These tests cover the functionality of the app3 module, which includes functions for logging actions to App5,
getting SFTP credentials, and sending emails.

"""

import unittest
from unittest.mock import patch, call
import requests
import logging
from io import StringIO
from app3 import get_credentials, send_email


def log_to_app5(action):
    """
    Log an action to App5.

    Parameters:
        action (str): The action to be logged.

    Returns:
        str: Log contents.

    """
    url = f'http://localhost:5000/log/{action}'
    headers = {'Content-Type': 'application/json'}
    data = {}

    logger = logging.getLogger(__name__)
    log_stream = StringIO()
    file_handler = logging.StreamHandler(log_stream)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        logger.info(f"PASS: Logged action into App5: {action}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to log action into App5: {e}")

    return log_stream.getvalue()


class TestLogToApp5(unittest.TestCase):
    """
    Test cases for the log_to_app5 function.

    """

    @patch('requests.post')
    def test_successful_log(self, mock_post):
        """
        Test successful logging to App5.

        """
        mock_post.return_value.status_code = 200

        log_contents = log_to_app5('test_action')

        mock_post.assert_called_once()
        mock_post.assert_called_with(
            'http://localhost:5000/log/test_action',
            json={},
            headers={'Content-Type': 'application/json'}
        )

        self.assertIn('PASS: Logged action into App5: test_action', log_contents)

    @patch('requests.post')
    def test_failed_log(self, mock_post):
        """
        Test failed logging to App5.

        """

        mock_post.side_effect = requests.exceptions.RequestException('Test error')

        log_contents = log_to_app5('another_action')

        mock_post.assert_called_once()
        mock_post.assert_called_with(
            'http://localhost:5000/log/another_action',
            json={},
            headers={'Content-Type': 'application/json'}
        )

        self.assertIn('Failed to log action into App5: Test error', log_contents)


class TestGetCredentials(unittest.TestCase):
    """
    Test cases for the get_credentials function.

    """

    @patch('builtins.input', return_value='test_user')
    @patch('getpass.getpass', return_value='test_password')
    def test_get_credentials(self, mock_pass, mock_input):
        """
        Test getting SFTP credentials.

        """
        # Call the function
        username, password = get_credentials()

        mock_input.assert_called_once_with("Enter your SFTP username: ")
        mock_pass.assert_called_once_with("Enter your SFTP password: ")

        self.assertEqual(username, 'test_user')
        self.assertEqual(password, 'test_password')


class TestApp3(unittest.TestCase):
    """
    Test cases for the send_email function in the app3 module.

    """

    @patch('smtplib.SMTP_SSL')
    @patch('builtins.input', return_value='test_user')
    @patch('getpass.getpass', return_value='test_password')
    def test_send_email(self, mock_pass, mock_input, mock_smtp):
        """
        Test sending emails with the send_email function.

        """
        from_address = 'vrp5109@psu.edu'
        to_addresses = ['vrp5109@psu.edu', 'drp5554@psu.edu']
        payload = 'Test payload'

        captured_output = StringIO()
        import sys
        sys.stdout = captured_output

        email_username = 'test_user'
        email_password = 'test_password'

        send_email(payload, email_username, email_password)

        sys.stdout = sys.__stdout__

        self.assertEqual(captured_output.getvalue().strip(), "Decoded payload sent via email to team members.")
        mock_smtp.assert_called_with('authsmtp.psu.edu', 465)

        expected_calls = [
            call(from_address, [to_addresses[0]], 'Content-Type: text/plain; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\nSubject: Decoded Payload from App2\nFrom: vrp5109@psu.edu\nTo: vrp5109@psu.edu\n\nDecoded Payload: Test payload'),
            call(from_address, [to_addresses[1]], 'Content-Type: text/plain; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\nSubject: Decoded Payload from App2\nFrom: vrp5109@psu.edu\nTo: drp5554@psu.edu\n\nDecoded Payload: Test payload')
        ]
        mock_smtp.return_value.sendmail.assert_has_calls(expected_calls, any_order=False)
        self.assertEqual(mock_smtp.return_value.quit.call_count, 2)


if __name__ == '__main__':
    unittest.main()
