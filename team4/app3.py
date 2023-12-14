# Project: Project Diamond -> App3 - Payload Verification, Transformation, and Transmission
# Purpose Details: Verify SFTP payload, email payload, transform using ORB, compress JSON object, log workflow to MongoDB
# Course: IST 411
# Author: Team 4
# Date Developed: 10/29/2023 
# Last Date Changed: 11/29/2023 
# Rev: 1 


import pysftp
import json
import hmac
import hashlib
import smtplib
from email.mime.text import MIMEText
import logging
from datetime import datetime
import getpass
import Pyro4
import requests

shared_key = b'team_four'

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def log_to_app5(action, error_message=None):
    """
    Logs actions and potential error messages to App5 via a POST request.

    Args:
    - action (str): The action to be logged.
    - error_message (str): Additional error details (default=None).
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
        if error_message:
            logging.error(f"{timestamp} - Additional error details: {error_message}")

def get_credentials():
    """
    Prompts the user for SFTP credentials.

    Returns:
    - username (str): SFTP username entered by the user.
    - password (str): SFTP password entered by the user.
    """
    username = input("Enter your SFTP username: ")
    password = getpass.getpass("Enter your SFTP password: ")
    return username, password

def send_single_email(fromAddress, toAddress, msg, smtp_server, smtp_port, email_username, email_password):
    """
    Sends a single email.

    Args:
    - fromAddress (str): Sender's email address.
    - toAddress (str): Recipient's email address.
    - msg (MIMEText): Email content in MIMEText format.
    - smtp_server (str): SMTP server address.
    - smtp_port (int): SMTP port number.
    - email_username (str): Sender's email username.
    - email_password (str): Sender's email password.

    Returns:
    - error_message (str): Error message in case of failure (default=None).
    """
    try:
        s = smtplib.SMTP_SSL(smtp_server, smtp_port)
        s.login(email_username, email_password)
        s.sendmail(fromAddress, [toAddress], msg.as_string())
        s.quit()
    except smtplib.SMTPException as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_message = f"{timestamp} - Error: {str(e)}"
        logging.error(error_message)
        return error_message

def send_email(decoded_payload, email_username, email_password):
    """
    Sends an email containing the decoded payload to team members.

    Args:
    - decoded_payload (str): Decoded payload content.
    - email_username (str): Sender's email username.
    - email_password (str): Sender's email password.
    """
    try:
        fromAddress = 'vrp5109@psu.edu'
        team_members = ['vrp5109@psu.edu', 'drp5554@psu.edu']
        subject = 'Decoded Payload from App2'
        message_content = f'Decoded Payload: {decoded_payload}'

        smtp_server = 'authsmtp.psu.edu'
        smtp_port = 465

        for recipient in team_members:
            msg = MIMEText(message_content)
            msg['Subject'] = subject
            msg['From'] = fromAddress
            msg['To'] = recipient

            error_message = send_single_email(fromAddress, recipient, msg, smtp_server, smtp_port, email_username, email_password)
            if error_message:
                raise Exception(error_message)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"{timestamp} - Decoded payload sent via email to team members.")
        print("Decoded payload sent via email to team members.")

        # Log the action to App5
        log_to_app5('Sent_decoded_payload_via_email')

    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.error(f"{timestamp} - Failed to send email: {str(e)}")
        print(f"Failed to send email: {str(e)}")
        log_to_app5('Failed_to_send_email', str(e))

def main():
    """
    Main function for the App3 workflow.
    """
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    cinfo = {
        'cnopts': cnopts,
        'host': '172.29.135.40',
        'port': 1855
    }

    username, password = get_credentials()
    cinfo['username'] = username
    cinfo['password'] = password

    try:
        with pysftp.Connection(**cinfo) as sftp:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.info(f"{timestamp} - PASS: Connected to SFTP server")
            print("Connected to SFTP server")
            sftp.chdir("/home/team4/received")

            remote_path = "app2_payload.json"
            local_path = "/home/team4/app3_payload.json"

            sftp.get(remote_path, local_path)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.info(f"{timestamp} - PASS: Received {remote_path} from SFTP server and saved as app3_payload.json")
            print(f"Received {remote_path} from SFTP server and saved as app3_payload.json")

            try:
                with open(local_path, "r", encoding="utf-8") as json_file:
                    payload_data = json.load(json_file)
            except json.JSONDecodeError as json_error:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logging.error(f"{timestamp} - FAILED: Error loading JSON: {str(json_error)}")
                print(f"Failed to load JSON: {str(json_error)}")
                return

            received_payload = payload_data.get("payload")
            received_hash = payload_data.get("hash")

            h = hmac.new(shared_key, received_payload.encode('utf-8'), hashlib.sha256)
            calculated_hash = h.hexdigest()

            if calculated_hash == received_hash:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logging.info(f"{timestamp} - PASS: Payload integrity verified: Hash matches.")
                print("PASS: Payload integrity verified: Hash matches.")
                print("Received content: ")
                print(received_payload)

                # Save the decoded payload to app3_payload.json
                try:
                    with open(local_path, "w", encoding="utf-8") as json_file:
                        json.dump({"payload": received_payload}, json_file, indent=4)
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logging.info(f"{timestamp} - PASS: Saved decoded payload to app3_payload.json")
                    print("Saved decoded payload to app3_payload.json")

                    # Prompt for email username and password only once
                    email_username = input("Enter your email username: ")
                    email_password = getpass.getpass("Enter your email password: ")

                    # Send the decoded payload via email
                    send_email(received_payload, email_username, email_password)
                except Exception as save_error:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logging.error(f"{timestamp} - FAILED: Error saving decoded payload: {str(save_error)}")
                    print(f"Failed to save decoded payload: {str(save_error)}")

                # Transform JSON to Python object
                python_object = json.loads(received_payload)

                # Use Pyro ORB to send Python object to app4
                try:
                    uri = input("Enter the Pyro URI of the app4 object:\n").strip()
                    app4 = Pyro4.Proxy(uri)

                    # Send Python object to app4
                    app4.receive_python_object(python_object)
                except Pyro4.errors.PyroError as e:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logging.error(f"{timestamp} - Failed to connect to app4: {str(e)}")
                    log_to_app5('Failed_to_connect_to_app4', str(e))

            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logging.info(f"{timestamp} - PASS: Payload integrity verification failed: Hash does not match.")
                print("Payload integrity verification failed: Hash does not match.")
                log_to_app5('Failed_to_send_payload_via_email', 'Payload_integrity_verification_failed')

            sftp.close()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.info(f"{timestamp} - PASS: Closing SFTP connection")
            print("Closing SFTP connection")

    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.error(f"{timestamp} - App3 encountered an error: {str(e)}")
        print(f"App3 encountered an error: {str(e)}")

if __name__ == "__main__":
    main()
