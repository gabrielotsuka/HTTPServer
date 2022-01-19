import socket

HOST, PORT = '', 8080

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
        # Connects in the server host and port and send the message through the socket
        socket.connect((HOST, PORT))
        socket.sendall(b'Hello world!')
        data = socket.recv(1024) # Reads the server reply

    print('Received', repr(data))