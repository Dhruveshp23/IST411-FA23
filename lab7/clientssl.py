import socket
import ssl

try:
    print("Client connecting to localhost:8080 using SSL")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Wrap the socket with SSL/TLS, specifying the server's certificate
    ssl_sock = ssl.wrap_socket(
        s,
        ca_certs="server.crt",
        cert_reqs=ssl.CERT_REQUIRED
    )
    
    # Connect to the server
    ssl_sock.connect(('localhost', 8080))
    
    # Send data to the server
    data_to_send = "Hello, server!"
    ssl_sock.send(data_to_send.encode('utf-8'))
    
    # Receive and print the server's response
    data_received = ssl_sock.recv(1024).decode('utf-8')
    print("Received data from server:", data_received)

except Exception as e:
    print(e)

finally:
    # Close the SSL/TLS socket
    if 'ssl_sock' in locals():
        ssl_sock.close()
