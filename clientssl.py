import socket
import ssl
import urllib.request
import json

url = 'https://jsonplaceholder.typicode.com/posts/2'
try:
    response = urllib.request.urlopen(url)
    payload = response.read()
except Exception as e:
    print("Request Denied")
    print(e)

try:
    print("Client connecting on port 8080 using SSL")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Create an SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(cafile='server.crt')

    # Wrap the socket with SSL/TLS
    conn = context.wrap_socket(s, server_hostname='localhost')
    conn.connect(('localhost', 8080))

    # Send JSON payload
    conn.sendall(payload)
    print("Payload sent")
    print("TLS version:", conn.version())

except Exception as e:
    print("Client Failed")
    print(e)
finally:
    conn.close()
