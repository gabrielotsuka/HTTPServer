import socket

# PORT < 1024 can require superuser permissions.
HOST, PORT = '127.0.0.1', 8080

if __name__ == "__main__":
    # TCP connection configuration. AF_INET refers to ipv4 and SOCK_STREAM is the TCP connection
    listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listenSocket.bind((HOST, PORT))
    listenSocket.listen(1)
    print('Serving HTTP on port {PORT}...')

    while True:    
        clientConnection, clientAddress = listenSocket.accept()
        with clientConnection: # As it uses with statement, it's not necessary to call clien_connection.close()
            request_data = clientConnection.recv(1024)
            print(request_data.decode('utf-8'))

            http_response = b"""\
HTTP/1.1 200 OK

Hello world
            """
            clientConnection.sendall(http_response)
