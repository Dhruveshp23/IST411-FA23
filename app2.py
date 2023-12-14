
import socket
import hashlib
import hmac
import pysftp
from pymongo import MongoClient
import logging
from datetime import datetime

# Shared key for HMAC
shared_key = b'secret_key'  # Replace with your actual shared key

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(message)s')
logging.getLogger().addHandler(logging.NullHandler())

# Function to log actions into MongoDB
def log_to_mongodb(action, timestamp):
    try:
        client = MongoClient('localhost', 27017)
        db = client['team4']
        activity_log = db['activityd']
        activity_log.insert_one({'action': action, 'timestamp': timestamp})
        logging.info(f"{timestamp} - PASS: Logged action into MongoDB: {action}")
    except Exception as e:
        logging.error(f"{timestamp} - Failed to log action into MongoDB: {str(e)}")

# Function to receive JSON payload from App1 over TLS
def receive_json_over_tls():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', 8082))
            s.listen(5)
            while True:
                (clientsocket, address) = s.accept()
                json_received = clientsocket.recv(1024)

                if json_received:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_to_mongodb('Received JSON payload from App1', timestamp)

                    # Calculate HMAC SHA-256 hash of JSON payload
                    h = hmac.new(shared_key, json_received, hashlib.sha256)
                    hash_value = h.hexdigest()

                    # Print the received JSON payload to the terminal
                    print("Received JSON payload from App1:")
                    print(json_received.decode('utf-8'))

                    # Save the JSON payload and its hash to a file
                    with open('app2_payload.json', 'wb') as file:
                        file.write(json_received)
                        file.write(hash_value.encode('utf-8'))
                    logging.info(f"{timestamp} - PASS: Saved JSON payload and hash to a file")

                    # Send the payload and hash to App3 via SFTP
                    send_json_via_sftp('app2_payload.json', timestamp)

                    # Exit gracefully after payload is received, logged, and sent
                    break
    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.error(f"{timestamp} - App2 encountered an error: {str(e)}")

# Function to send JSON payload and hash to App3 via SFTP
def send_json_via_sftp(file_path, timestamp):
    try:
        username = 'drp5554'
        password = 'Dhruvesh@22'
        host = '172.29.135.40'
        port = 1855

        # Create an instance of CnOpts and set hostkeys to None (disable host key checking)
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        # Define the connection information
        cinfo = {
            'cnopts': cnopts,
            'host': host,
            'port': port,
            'username': username,
            'password': password
        }

        with pysftp.Connection(**cinfo) as sftp:
            sftp.put(file_path, '/home/drp5554/app2_payload.json')
            logging.info(f"{timestamp} - PASS: Sent JSON payload and hash to App3 via SFTP")
    except Exception as e:
        logging.error(f"{timestamp} - Failed to send data to App3 via SFTP: {str(e)}")

if __name__ == "__main__":
    receive_json_over_tls()


