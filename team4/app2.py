# Project: Project Diamond -> App2 - Secure Payload Handling and Transmission
# Purpose Details: Receive secure payload via TLS, hash using HMAC, send via secure SFTP, log workflow to MongoDB
# Course: IST 411
# Author: Team 4
# Date Developed: 10/08/2023 
# Last Date Changed: 11/29/2023 
# Rev: 1 
import socket
import hashlib
import hmac
import pysftp
from pymongo import MongoClient
import logging
from datetime import datetime
import json
import getpass
import requests
import os
shared_key = b'team_four'

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(message)s')
logging.getLogger().addHandler(logging.NullHandler())

def log_to_app5(action):
    """
    Log an action to App5 via HTTP POST request and record it in a log file.

    Args:
    - action (str): The action to be logged in App5.
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

def get_sftp_credentials():
    """
    Prompt user for SFTP credentials.

    Returns:
    - username (str): SFTP username.
    - password (str): SFTP password (securely obtained).
    """
    username = input("\nEnter your SFTP username: ")
    password = getpass.getpass("Enter your SFTP password: ")
    return username, password

def receive_json_over_tls():
    """
    Listen for JSON data over TLS from App1 and process it.
    """
    try:
        print("App2 is now running and listening to App1")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', 8082))
            s.listen(5)
            while True:
                (clientsocket, address) = s.accept()
                json_received = clientsocket.recv(1024)

                if json_received:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_to_app5('Received_JSON_from_App1')

                    h = hmac.new(shared_key, json_received, hashlib.sha256)
                    hash_value = h.hexdigest()

                    payload_with_hash = {
                        "payload": json_received.decode('utf-8'),
                        "hash": hash_value
                    }

                    print("\nReceived JSON payload from App1:")
                    print(json_received.decode('utf-8'))

                    # Save the app2_payload.json file in the 'received' fold>
                    received_folder = 'received'
                    os.makedirs(received_folder, exist_ok=True)
                    file_path = os.path.join(received_folder, 'app2_payload.json')

#                    print(f"File path: {file_path}")

                    with open(file_path, 'w') as file:
                        json.dump(payload_with_hash, file, indent=2)

                    logging.info(f"{timestamp} - PASS: Saved JSON payload and hash to a file")
                    print("\nPASS: Saved JSON payload and hash to an app2_payload.json file.")
                    send_json_via_sftp(file_path, timestamp)

                    break
    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_to_app5('app2_error')

def send_json_via_sftp(file_path, timestamp):
    """
    Send JSON payload and hash to App3 via SFTP.

    Args:
    - file_path (str): Path to the JSON payload file.
    - timestamp (str): Timestamp of the action.
    """

    try:
        username, password = get_sftp_credentials()
        host = '172.29.135.40'
        port = 1855

        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        cinfo = {
            'cnopts': cnopts,
            'host': host,
            'port': port,
            'username': username,
            'password': password
        }

        with pysftp.Connection(**cinfo) as sftp:
            sftp.put(file_path, './app2_payload.json')
            logging.info(f"{timestamp} - PASS: Sent JSON payload and hash to App3 via SFTP")
            print("PASS: Sent JSON payload and hash to App3 via SFTP")

            log_to_app5('Sent_JSON_to_App3')
    except Exception as e:
        logging.error(f"{timestamp} - Failed to send data to App3 via SFTP: {str(e)}")
        print(f"Failed to send data to App3 via SFTP: {str(e)}")
        log_to_app5('Failed_to_send_JSON_to_App3')

if __name__ == "__main__":
    receive_json_over_tls()
