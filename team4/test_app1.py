# Project: Project Diamond 
# Purpose Details: Unit tests for App 1 of Project Diamond.  
# Course: IST 411 
# Author: Team 4 
# Date Developed: 10/08/2023 
# Last Date Changed: 11/29/2023 
# Rev: 1


import unittest
from unittest.mock import patch, Mock
import app1

class TestApp1(unittest.TestCase):
    """
    A TestCase class for testing functions in the 'app1' module.
    """

    @patch('app1.requests.get')
    def test_get_json_payload_fail(self, mock_get):
        """
        Test case to simulate failure when retrieving JSON payload.

        This test mocks the 'requests.get' method to simulate a connection failure
        and ensures that the expected exception is raised.

        Args:
        - mock_get: Mock object of 'requests.get' method.

        Returns:
        None
        """
        mock_get.side_effect = Exception('Failed to connect')

        with self.assertRaises(Exception) as context:
            app1.get_json_payload('http://example.com')

    @patch('app1.log_to_app5')
    @patch('socket.socket')
    def test_send_json_to_app2_fail(self, mock_socket, mock_log_to_app5):
        """
        Test case to simulate failure when sending JSON payload to App2.

        This test mocks the 'socket.socket' and simulates a connection failure
        to ensure that the expected exception is raised.

        Args:
        - mock_socket: Mock object of 'socket.socket'.
        - mock_log_to_app5: Mock object of 'log_to_app5' method.

        Returns:
        None
        """
        json_payload = '{"key": "value"}'

        mock_socket_instance = mock_socket.return_value.__enter__.return_value
        mock_socket_instance.connect.return_value = None
        mock_socket_instance.sendall.side_effect = Exception('Failed to send data')

        with self.assertRaises(Exception) as context:
            app1.send_json_to_app2(json_payload)
            print(context.exception)

        mock_log_to_app5.assert_called_once_with('send_json_to_app2_fail')

        mock_socket_instance.connect.assert_called_once()
        # Assert that the mocked socket.sendall method was called
        mock_socket_instance.sendall.assert_called_once()

    @patch('app1.requests.post')
    @patch('socket.socket')
    def test_send_json_to_app2_success(self, mock_socket, mock_post):
        """
        Test case for successful sending of JSON payload to App2.

        This test mocks the 'socket.socket' and 'requests.post' methods
        to simulate a successful connection and ensures that the function executes
        without raising an exception.

        Args:
        - mock_socket: Mock object of 'socket.socket'.
        - mock_post: Mock object of 'requests.post' method.

        Returns:
        None
        """
        json_payload = '{"userId": 1, "id": 1, "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit", "body": "quia et suscipit\\nsuscipit recusandae consequuntur expedita et cum\\nreprehenderit molestiae ut ut quas totam\\nostrum rerum est autem sunt rem eveniet architecto"}'

        mock_socket_instance = mock_socket.return_value.__enter__.return_value
        mock_socket_instance.connect.return_value = None
        mock_post.return_value.status_code = 200

        app1.send_json_to_app2(json_payload)

        mock_socket_instance.connect.assert_called_once()
        mock_post.assert_called_once()

if __name__ == '__main__':
    unittest.main()
