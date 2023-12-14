# Project: Project Diamond 
# Purpose Details: Unit tests for APP 2 of Project Diamond  
# Course: IST 411 
# Author: Team 4 
# Date Developed: 10/08/2023 
# Last Date Changed: 11/29/2023 
# Rev: 1 

import unittest
from unittest.mock import patch
import datetime
import requests
import logging
import pysftp
import json
import hashlib
import getpass
from app2 import receive_json_over_tls

# Define a shared key for authentication
shared_key = b'team_four'

# Configure logging to a file named app.log
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(message)s')
logging.getLogger().addHandler(logging.NullHandler())

def log_to_app5(action):
    """
    Logs an action to App5 by sending a POST request.

    Args:
    - action (str): The action to be logged.

    Sends a POST request to App5's local URL to log the action.
    """
    url = f'http://localhost:5000/log/{action}'
    data = {}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"{timestamp} - PASS: Logged action into App5: {action}")
    except requests.exceptions.RequestException as e:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.error(f"{timestamp} - Failed to log action into App5: {str(e)}")

def get_sftp_credentials():
    """
    Prompts the user for SFTP credentials (username and password).

    Returns:
    - username (str): SFTP username entered by the user.
    - password (str): SFTP password entered by the user.
    """
    username = input("\nEnter your SFTP username: ")
    password = getpass.getpass("Enter your SFTP password: ")
    return username, password

def send_json_via_sftp(file_path, timestamp, sftp_username, sftp_password):
    """
    Sends a JSON file via SFTP to a specified location.

    Args:
    - file_path (str): Path to the JSON file.
    - timestamp (str): Timestamp for identification.
    - sftp_username (str): SFTP username for authentication.
    - sftp_password (str): SFTP password for authentication.

    Returns:
    - success (bool): Indicates whether SFTP upload was successful.
    """
    try:
        srv = pysftp.Connection('172.29.135.40', username=sftp_username, password=sftp_password)
        remote_path = f'/home/vrp5109/dteam/{file_path}'
        srv.put(file_path, remote_path)
        srv.close()
        return True
    except Exception as e:
        return False

class TestApp(unittest.TestCase):
    @patch('requests.post')
    def test_successful_logging(self, mock_post):
        """
        Test successful logging to App5.

        Mocks the requests.post method to simulate a successful log to App5.
        """
        action = "Test action"
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        log_to_app5(action)

        mock_post.assert_called_once()
        self.assertEqual(mock_post.call_args[1]['json'], {})
        self.assertEqual(mock_post.call_args[1]['headers'], {'Content-Type': 'application/json'})

    @patch('requests.post')
    def test_failed_logging(self, mock_post):
        """
        Test failed logging to App5.

        Mocks the requests.post method to simulate a failed log to App5.
        """
        action = "Test action"
        mock_post.side_effect = requests.exceptions.RequestException("Failed to connect")

        log_to_app5(action)

        mock_post.assert_called_once()

    def test_get_sftp_credentials(self):
        """
        Test the retrieval of SFTP credentials.

        Uses patch to mock user input and getpass to simulate SFTP credential entry.
        """
        with patch('builtins.input', return_value='test_user'), \
             patch('getpass.getpass', return_value='test_password'):
            username, password = get_sftp_credentials()

        self.assertEqual(username, 'test_user')
        self.assertEqual(password, 'test_password')

    @patch('pysftp.Connection')
    def test_successful_sending(self, mock_sftp):
        """
        Test successful JSON file sending via SFTP.

        Mocks the pysftp.Connection to simulate a successful file transfer via SFTP.
        """
        self.file_path = 'app2_payload.json'
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        send_json_via_sftp(self.file_path, self.timestamp, 'test_user', 'test_password')

        mock_sftp.return_value.put.assert_called_once_with(self.file_path, '/home/vrp5109/dteam/app2_payload.json')

    @patch('pysftp.Connection')
    def test_failed_sending(self, mock_sftp):
        """
        Test failed JSON file sending via SFTP.

        Mocks the pysftp.Connection to simulate a failed file transfer via SFTP.
        """
        self.file_path = 'app2_payload.json'
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mock_sftp.return_value.put.side_effect = Exception('SFTP connection failed')
        send_json_via_sftp(self.file_path, self.timestamp, 'test_user', 'test_password')

        self.assertEqual(mock_sftp.return_value.put.call_count, 1)

if __name__ == '__main__':
    unittest.main()
