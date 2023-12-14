# Project: App5 - RESTful Service Handling
# Purpose Details: Receive log requests via Eve RESTful service, store in MongoDB, handle pass and fail method handlers, log workflow to MongoDB
# Course: IST 411
# Author: Team 4
# Date Developed: 10/29/2023 
# Last Date Changed: 11/29/2023 
# Rev: 1 


import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request
from pymongo import MongoClient

# Initialize logging
log_file = 'app5.log'
log_level = logging.DEBUG
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger(__name__)
logger.setLevel(log_level)
file_handler = RotatingFileHandler(log_file, maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(file_handler)

# Initialize MongoDB client and collection
client = MongoClient('localhost', 27017)
db = client['team4']
logs_collection = db['diamondlogs']

# Initialize Flask app
app = Flask(__name__)

# Route for logging actions from App1
@app.route('/log/retrieve_json', methods=['POST'])
def log_retrieve_json_from_app1():
    """
    Log retrieval of JSON data from App1.
    """
    try:
        logger.info('Action: retrieve_json_from_app1 - PASS')
        log_entry = {
            'action': 'retrieve_json_from_app1',
            'source': 'App1',
            'message': 'Action: retrieve_json_from_app1',
            'status': 'PASS',
        }
        logs_collection.insert_one(log_entry)
        return 'Action "retrieve_json_from_app1" logged successfully from App1 - PASS', 201
    except Exception as e:
        logger.error(f'Action: retrieve_json_from_app1 - FAIL - {str(e)}')
        return str(e), 500

# Route for logging successful JSON transmission from App1 to App2
@app.route('/log/send_json_to_app2_success', methods=['POST'])
def log_send_json_to_app2_success_from_app1():
    """
    Log successful transmission of JSON from App1 to App2.
    """
    try:
        logger.info('Action: send_json_to_app2_success_from_app1 - PASS')
        log_entry = {
            'action': 'send_json_to_app2_success_from_app1',
            'source': 'App1',
            'message': 'Action: send_json_to_app2_success_from_app1',
            'status': 'PASS',
        }
        logs_collection.insert_one(log_entry)
        return 'Action "send_json_to_app2_success_from_app1" logged successfully from App1 - PASS', 201
    except Exception as e:
        logger.error(f'Action: send_json_to_app2_success_from_app1 - FAIL - {str(e)}')
        return str(e), 500

# Route for logging successful receipt of Python object from App4
@app.route('/log/receive_python_object_success_from_app4', methods=['POST'])
def log_receive_python_object_success_from_app4():
    """
    Log successful receipt of a Python object from App4.
    """
    try:
        logger.info('Action: receive_python_object_success_from_app4 - PASS')
        log_entry = {
            'action': 'receive_python_object_success_from_app4',
            'source': 'App4',
            'message': 'Action: receive_python_object_success_from_app4',
            'status': 'PASS',
        }
        logs_collection.insert_one(log_entry)
        return 'Action "receive_python_object_success_from_app4" logged successfully from App4 - PASS', 201
    except Exception as e:
        logger.error(f'Action: receive_python_object_success_from_app4 - FAIL - {str(e)}')
        return str(e), 500

# Routes for logging actions from App3
@app.route('/log/Sent_payload_via_email', methods=['POST'])
def log_sent_payload_via_email():
    """
    Log the action of sending a payload via email from App3.
    """
    try:
        logger.info('Action: Sent_payload_via_email - PASS')
        log_entry = {
            'action': 'Sent_payload_via_email',
            'source': 'App3',
            'message': 'Action: Sent_payload_via_email',
            'status': 'PASS',
        }
        logs_collection.insert_one(log_entry)
        return 'Action "Sent_payload_via_email" logged successfully from App3 - PASS', 201
    except Exception as e:
        logger.error(f'Action: Sent_payload_via_email - FAIL - {str(e)}')
        return str(e), 500

@app.route('/log/Sent_decoded_payload_via_email', methods=['POST'])
def log_sent_decoded_payload_via_email():
    """
    Log the action of sending a decoded payload via email from App3.
    """
    try:
        logger.info('Action: Sent_decoded_payload_via_email - PASS')
        log_entry = {
            'action': 'Sent_decoded_payload_via_email',
            'source': 'App3',
            'message': 'Action: Sent_decoded_payload_via_email',
            'status': 'PASS',
        }
        logs_collection.insert_one(log_entry)
        return 'Action "Sent_decoded_payload_via_email" logged successfully from App3 - PASS', 201
    except Exception as e:
        logger.error(f'Action: Sent_decoded_payload_via_email - FAIL - {str(e)}')
        return str(e), 500

# Routes for logging actions from App2
@app.route('/log/Received_JSON_from_App1', methods=['POST'])
def log_received_json_from_app1():
    """
    Log receiving JSON from App1 by App2.
    """
    try:
        logger.info('Action: Received_JSON_from_App1 - PASS')
        log_entry = {
            'action': 'Received_JSON_from_App1',
            'source': 'App1',
            'message': 'Action: Received_JSON_from_App1',
            'status': 'PASS',
        }
        logs_collection.insert_one(log_entry)
        return 'Action "Received_JSON_from_App1" logged successfully from App1 - PASS', 201
    except Exception as e:
        logger.error(f'Action: Received_JSON_from_App1 - FAIL - {str(e)}')
        return str(e), 500

@app.route('/log/Sent_JSON_to_App3', methods=['POST'])
def log_sent_json_to_app3():
    """
    Log sending JSON to App3 from App2.
    """
    try:
        logger.info('Action: Sent_JSON_to_App3 - PASS')
        log_entry = {
            'action': 'Sent_JSON_to_App3',
            'source': 'App2',
            'message': 'Action: Sent_JSON_to_App3',
            'status': 'PASS',
        }
        logs_collection.insert_one(log_entry)
        return 'Action "Sent_JSON_to_App3" logged successfully from App2 - PASS', 201
    except Exception as e:
        logger.error(f'Action: Sent_JSON_to_App3 - FAIL - {str(e)}')
        return str(e), 500

@app.route('/log/Failed_to_send_JSON_to_App3', methods=['POST'])
def log_failed_to_send_json_to_app3():
    """
    Log failure in sending JSON to App3 from App2.
    """
    try:
        logger.error('Action: Failed_to_send_JSON_to_App3 - PASS')
        log_entry = {
            'action': 'Failed_to_send_JSON_to_App3',
            'source': 'App2',
            'message': 'Action: Failed_to_send_JSON_to_App3',
            'status': 'PASS',
        }
        logs_collection.insert_one(log_entry)
        return 'Action "Failed_to_send_JSON_to_App3" logged successfully from App2 - PASS', 201
    except Exception as e:
        logger.error(f'Action: Failed_to_send_JSON_to_App3 - FAIL - {str(e)}')
        return str(e), 500

if __name__== '__main__':
    app.run()
