# Project: Lab 5 Client and Server Using Networking Sockets
# Purpose Details: To learn how clients connect to servers using networking
# Course: IST 411
# Author: Dhruvesh PAtel
# Date Developed:09/20/2023
# Last Date Changed:
# Rev:

import socket
import json

# Create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('', 8080)

try:
    # Bind the socket to the server address and port
    serversocket.bind(server_address)

    # Listen for incoming connections
    serversocket.listen(1)
    print("Server is listening on port 8080...")

    # Accept incoming connection
    clientsocket, addr = serversocket.accept()
    print(f"Accepted connection from {addr}")

    # Receive the JSON payload from the client
    json_payload = clientsocket.recv(1024).decode('utf-8')
    payload = json.loads(json_payload)

    print("Received JSON payload:")
    print(payload)

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    # Close the client socket
    clientsocket.close()
    # Close the server socket
    serversocket.close()
