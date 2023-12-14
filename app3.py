import pysftp
import hashlib
import hmac
import threading
from pymongo import MongoClient
import smtplib
from email.mime.text import MIMEText
import logging
from datetime import datetime

# Shared key for HMAC
shared_key = b'secret_key'  # Replace with your actual shared key

# Configure logging
logging.basicConfig(filename='app3.log', level=logging.INFO, format='%(message)s')
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

# Function to verify the HMAC hash
def verify_hmac(json_payload, received_hash):
    h = hmac.new(shared_key, json_payload, hashlib.sha256)
    calculated_hash = h.hexdigest()
    return calculated_hash == received_hash

# Function to send email
def send_email(subject, message_content):
    fromAddress = 'drp5554@psu.edu'
    toAddress = 'drp5554@psu.edu'

    msg = MIMEText(message_content)
    msg['Subject'] = subject
    msg['From'] = fromAddress
    msg['To'] = toAddress

    try:
        s = smtplib.SMTP_SSL('authsmtp.psu.edu', 465)
        s.sendmail(fromAddress, [toAddress], msg.as_string())
        logging.info("Email sent successfully.")
    except smtplib.SMTPException as e:
        logging.error("Error sending email: " + str(e))
    finally:
        s.quit()

# Function to process the received JSON payload
def process_payload(json_payload, received_hash, timestamp):
    if verify_hmac(json_payload, received_hash):
        log_to_mongodb('Verified HMAC hash', timestamp)
        logging.info("Payload received and HMAC hash verified.")
        subject = 'Payload Received and Verified'
        message_content = 'Payload received and HMAC hash verified.'
    else:
        log_to_mongodb('Failed to verify HMAC hash', timestamp)
        logging.error("Payload received, but HMAC hash verification failed.")
        subject = 'Payload Received but Verification Failed'
        message_content = 'Payload received, but HMAC hash verification failed.'

    # Email team members using threading
    email_thread = threading.Thread(target=send_email, args=(subject, message_content))
    email_thread.start()

# Main function
def main():
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Establish an SFTP connection to receive the payload
        username = 'drp5554'
        password = 'Dhruvesh@22'
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
            sftp.chdir('/home/drp5554')
            file_path = '/home/drp5554/app2_payload.json'
            received_hash = None
            payload = None

            # Check for the file and its hash
            files = sftp.listdir()
            for file in files:
                if file == 'app2_payload.json':
                    with sftp.file('app2_payload.json') as remote_file:
                        data = remote_file.read()
                        received_hash = data[-64:]
                        payload = data[:-64]

            if payload and received_hash:
                # Process the payload
                process_payload(payload, received_hash, timestamp)
            else:
                logging.error("Payload not found or hash missing.")

    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.error(f"{timestamp} - App3 encountered an error: {str(e)}")

if __name__ == "__main__":
    main()
