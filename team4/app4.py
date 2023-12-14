# Project: Diamond Project -> App4 - Data Transformation and Queue Handling
# Purpose Details: Transform Pyro object, queue using RabbitMQ, display round trip time, log workflow to MongoDB
# Course: IST 411
# Author: Team 4
# Date Developed: 11/26/2023 
# Last Date Changed: 11/29/2023 
# Rev: 1


import Pyro4
import json
import logging
from datetime import datetime
import requests

class App4Receiver:
    """
    App4Receiver class receives and processes Python objects.
    """

    @Pyro4.expose
    def receive_python_object(self, python_object):
        """
        receive_python_object receives a Python object, converts it to JSON,
        and logs the action to App5.

        Args:
        - python_object: Python object to be processed.

        Returns:
        None
        """
        try:
            # Convert Python object to JSON
            json_data = json.dumps(python_object, indent=2)
            print("Received Python object:")
            print(json_data)

            # Log to App5
            log_to_app5('receive_python_object_success_from_app4')

        except Exception as e:
            print(f"An error occurred during Python object processing: {e}")
            log_to_app5('failed_to_process_python_object')

def log_to_app5(action):
    """
    log_to_app5 logs an action to App5 via HTTP POST request.

    Args:
    - action: Action to be logged to App5.

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

def main():
    """
    Main function to start the Pyro4 server.
    """
    daemon = None
    try:
        daemon = Pyro4.Daemon()
        uri = daemon.register(App4Receiver)

        with Pyro4.locateNS() as ns:
            ns.register("example.app4receiver", uri)

        print("Server is ready. Object URI =", uri)

        # Keep the server running
        daemon.requestLoop()

    except Pyro4.errors.NamingError:
        print("Error: Failed to locate the Pyro4 nameserver. Make sure the nameserver is running.")
    except Pyro4.errors.PyroError as e:
        print(f"Pyro4 Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if daemon is not None:
            daemon.shutdown()

if __name__ == "__main__":
    main()
