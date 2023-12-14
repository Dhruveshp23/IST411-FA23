import socket
import ssl
import json
import signal
import sys

# Server configuration
host = 'localhost'
port = 8080
server_certfile = 'server.crt'
server_keyfile = 'server.key'

# Create an SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile=server_certfile, keyfile=server_keyfile)

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)

def handle_client(client_socket):
    try:
        conn = context.wrap_socket(client_socket, server_side=True)
        print("Connected by", conn.getpeername())
        print("TLS version:", conn.version())

        data = conn.recv(1024).decode('utf-8')
        print("Received data from client:", data)

        # Process the JSON payload
        try:
            json_data = json.loads(data)
            print("JSON payload received:", json_data)
        except json.JSONDecodeError:
            print("Invalid JSON data received")

        # Send a response back to the client
        response_data = json.dumps({"response": "Hello, client!"})
        conn.send(response_data.encode('utf-8'))

    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()

def exit_handler(sig, frame):
    print("Server is shutting down...")
    server_socket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, exit_handler)

print("Server listening on {}:{}".format(host, port))

while True:
    client_sock, client_addr = server_socket.accept()
    handle_client(client_sock)
