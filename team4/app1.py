# Project: App1 - Data Retrieval and Transmission
# Purpose Details: Retrieve JSON payload via CURL, transmit securely using TLS via network sockets, save payload to file, log workflow to MongoDB
# Course: IST 411
# Author: Team 4
# Date Developed: 10/8/2023 
# Last Date Changed: 11/29/2023 
# Rev: 5 

"""
app1.py: Module for performing various actions.

This module provides functions for logging actions, retrieving JSON data, and sending JSON data to App2.

Author: Team4
"""

import requests
import json
import logging
from datetime import datetime
import socket

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(message)s')

def log_to_app5(action):
    """
    Log an action to App5.

    Args:
        action (str): The action to be logged.

    Returns:
        None
    """
    url = f'http://localhost:5000/log/{action}'
    data = {}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"{timestamp} - PASS: Logged action into App5: {action}")
    except requests.exceptions.RequestException as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.error(f"{timestamp} - Failed to log action into App5: {str(e)}")

def get_json_payload(url):
    """
    Retrieve JSON payload from the specified URL.

    Args:
        url (str): The URL to retrieve JSON data from.

    Returns:
        dict or None: The JSON payload if successful, None otherwise.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_to_app5('retrieve_json')
        return response.json()
    except requests.exceptions.RequestException as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_to_app5('retrieve_json_fail')
        return None

def send_json_to_app2(json_payload):
    """
    Send JSON payload to App2 using a socket connection.

    Args:
        json_payload (str): The JSON payload to be sent.

    Returns:
        None
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('127.0.0.1', 8082))
            s.sendall(json_payload.encode('utf-8'))

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_to_app5('send_json_to_app2_success')  # Updated endpoint
    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_to_app5('send_json_to_app2_fail')

def main():
    """
    Main function to execute the script.

    Returns:
        None
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        url = 'https://jsonplaceholder.typicode.com/posts/1/'
        payload = get_json_payload(url)

        if payload:
            with open('app1_payload.json', 'w') as file:
                json.dump(payload, file)
            logging.info(f"{timestamp} - PASS: Saved JSON payload to a file")

            json_payload = json.dumps(payload)
            send_json_to_app2(json_payload)

    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_to_app5('app1_error')

if __name__ == "__main__":
    main()
