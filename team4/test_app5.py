# Project: Project Diamond 
# Purpose Details: Unit tests for App5 of Project Diamond  
# Course: IST 411 
# Author: Team 4 
# Date Developed: 10/29/2023 
# Last Date Changed: 11/29/2023 
# Rev: 1

import unittest
import json
from app5 import app

class App5TestCase(unittest.TestCase):
    """
    Test case for various functionalities in the app5 module.
    """

    def setUp(self):
        """
        Set up the test client and configure app for testing.
        """
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        """
        Clean up after each test.
        """
        pass

    def test_log_retrieve_json_from_app1(self):
        """
        Test logging retrieval of JSON from app1.
        """
        data = {
        }

        response = self.app.post('/log/retrieve_json', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Action "retrieve_json_from_app1" logged successfully from App1 - PASS', response.data)

    def test_log_send_json_to_app2_success_from_app1(self):
        """
        Test logging successful sending of JSON to app2 from app1.
        """
        data = {
        }

        response = self.app.post('/log/send_json_to_app2_success', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Action "send_json_to_app2_success_from_app1" logged successfully from App1 - PASS', response.data)

    def test_log_receive_python_object_success_from_app4(self):
        """
        Test logging successful receipt of a Python object from app4.
        """
        data = {
        }

        response = self.app.post('/log/receive_python_object_success_from_app4', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Action "receive_python_object_success_from_app4" logged successfully from App4 - PASS', response.data)

    def test_log_sent_payload_via_email(self):
        """
        Test logging the sending of a payload via email from app3.
        """
        data = {
        }

        response = self.app.post('/log/Sent_payload_via_email', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Action "Sent_payload_via_email" logged successfully from App3 - PASS', response.data)

    def test_log_received_json_from_app1(self):
        """
        Test logging the receipt of JSON from app1.
        """
        data = {
        }

        response = self.app.post('/log/Received_JSON_from_App1', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Action "Received_JSON_from_App1" logged successfully from App1 - PASS', response.data)

    def test_log_sent_json_to_app3(self):
        """
        Test logging the sending of JSON to app3.
        """
        data = {
        }

        response = self.app.post('/log/Sent_JSON_to_App3', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Action "Sent_JSON_to_App3" logged successfully from App2 - PASS', response.data)

    def test_log_failed_to_send_json_to_app3(self):
        """
        Test logging the failure to send JSON to app3.
        """
        data = {
        }

        response = self.app.post('/log/Failed_to_send_JSON_to_App3', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Action "Failed_to_send_JSON_to_App3" logged successfully from App2 - PASS', response.data)

if __name__ == '__main__':
    unittest.main()
