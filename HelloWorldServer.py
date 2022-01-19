import socket

# HOST string vazia aceitará conexão com todas interfaces ipv4 disponíveis
# PORT < 1024 pode exigir permissões de super usuário.
HOST, PORT = '127.0.0.1', 8080

if __name__ == "__main__":
    # Configuração conexão TCP. AF_INET se refere ao ipv4 e SOCK_STREAM é a conexão TCP
    # with usado portanto não é necessária a chamada de listen_socket.close()
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(1)
    print('Serving HTTP on port {PORT}...')

    while True:    
        client_connection, client_address = listen_socket.accept()
        with client_connection:
            request_data = client_connection.recv(1024)
            print(request_data.decode('utf-8'))

            http_response = b"""\
HTTP/1.1 200 OK

Hello world
            """
            client_connection.sendall(http_response)
