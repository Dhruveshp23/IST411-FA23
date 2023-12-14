import requests
import json
import logging
from pymongo import MongoClient
from datetime import datetime
import socket

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(message)s')

# Function to log actions into MongoDB with timestamps
def log_to_mongodb(action, timestamp):
    try:
        client = MongoClient('localhost', 27017)
        db = client['team4']
        activity_log = db['activityd']
        activity_log.insert_one({'action': action, 'timestamp': timestamp})
        logging.info(f"{timestamp} - PASS: Logged action into MongoDB: {action}")
    except Exception as e:
        logging.error(f"{timestamp} - Failed to log action into MongoDB: {str(e)}")

# Function to retrieve JSON payload from a URL
def get_json_payload(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"{timestamp} - PASS: Retrieving JSON payload from the internet")
        return response.json()
    except requests.exceptions.RequestException as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.error(f"{timestamp} - Failed to retrieve JSON payload from the internet: {str(e)}")
        return None

# Function to send JSON payload to App2
def send_json_to_app2(json_payload):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('127.0.0.1', 8082))
            s.sendall(json_payload.encode('utf-8'))

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"{timestamp} - PASS: Sent JSON payload to App2")
    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.error(f"{timestamp} - Failed to send data to App2: {str(e)}")

# Main function
def main():
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Retrieve JSON payload from the Internet securely with SSL verification
        url = 'https://jsonplaceholder.typicode.com/posts/1/comments'
        payload = get_json_payload(url)

        if payload:
            # Log actions into MongoDB
            log_to_mongodb('Retrieving JSON payload from the internet', timestamp)
            log_to_mongodb('Saved JSON payload to a file', timestamp)
            log_to_mongodb('Sent JSON payload to App2', timestamp)

            # Save JSON payload to a file
            with open('app1_payload.json', 'w') as file:
                json.dump(payload, file)
            logging.info(f"{timestamp} - PASS: Saved JSON payload to a file")

            # Send JSON payload to App2
            json_payload = json.dumps(payload)
            send_json_to_app2(json_payload)
    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.error(f"{timestamp} - PASS: App1 encountered an error: {str(e)}")

if __name__ == "__main__":
    main()
