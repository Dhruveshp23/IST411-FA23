# Project: Lab 5 Client and Server Using Networking Sockets
# Purpose Details: To learn how clients connect to servers using networking
# Course: IST 411
# Author: Your Name
# Date Developed:
# Last Date Changed:
# Rev:

import socket
import json

# Create a socket object
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('localhost', 8080)

try:
    # Connect to the server
    clientsocket.connect(server_address)

    # Create a sample JSON payload
    json_payload = {
        "postId": 1,
        "id": 1,
        "name": "id labore ex et quam laborum",
        "email": "Eliseo@gardner.biz",
        "body": "laudantium enim quasi est quidem magnam voluptate ipsam eos\ntempora quo necessitatibus\ndolor quam autem quasi\nreiciendis e>"
    }

    # Send the JSON payload to the server
    clientsocket.sendall(json.dumps(json_payload).encode('utf-8'))

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    # Close the client socket
    clientsocket.close()

