import socket

# PORT < 1024 can require superuser permissions.
HOST, PORT = '127.0.0.1', 8080

if __name__ == "__main__":
    # TCP connection configuration. AF_INET refers to ipv4 and SOCK_STREAM is the TCP connection
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(1)
    print('Serving HTTP on port {PORT}...')

    while True:    
        client_connection, client_address = listen_socket.accept()
        with client_connection: # As it uses with statement, it's not necessary to call clien_connection.close()
            request_data = client_connection.recv(1024)
            print(request_data.decode('utf-8'))

            http_response = b"""\
HTTP/1.1 200 OK

Hello world
            """
            client_connection.sendall(http_response)
