from logging import exception
import socket

# PORT < 1024 can require superuser permissions.
HOST, PORT = '127.0.0.1', 8080

def buildResponse():
    return b"""\
HTTP/1.1 200 OK

Hello world
            """

if __name__ == "__main__":
    # TCP connection configuration. AF_INET refers to ipv4 and SOCK_STREAM is the TCP connection
    listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listenSocket.bind((HOST, PORT))
    listenSocket.listen(1)
    print('Serving HTTP on port ' + str(PORT))

    while True:    
        clientConnection, clientAddress = listenSocket.accept()
        with clientConnection: # As it uses with statement, it's not necessary to call clientConnection.close()
            requestData = clientConnection.recv(4096).decode('utf-8')
            fileName = requestData[5:requestData.find("HTTP/1.1")-1]
            if fileName != 'favicon.ico':
                if fileName == '':
                    print('Invalid Path URL. Please insert a path in the following format: localhost:' + str(PORT) + '/<file_name.ext>')
                    clientConnection.sendall(buildResponse())
                    continue
                try:
                    with open(fileName, 'rb') as f:
                        file = f.read()
                        print('cheguei aqui')
                except FileNotFoundError:
                    print('File ' + fileName + ' not found')

            clientConnection.sendall(buildResponse())
