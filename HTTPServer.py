import socket
import threading
import resource
from os import path

# PORT < 1024 can require superuser permissions.
HOST = ''

H1 = 'HTTP/1.1 '
HCT = 'Content-Disposition: attachment; filename='

NOT_FOUND = '404 Not Found'
BAD_REQUEST = '400 Bad Request'
OK = '200 OK'

resource.setrlimit(resource.RLIMIT_NOFILE, (4096, 4096))
mutex = threading.Lock()

def buildErrorMessage(message, httpStatus):
    response = f"\n{H1}{httpStatus}\n\n{message}\n"
    return bytearray(response, 'utf-8')

def buildHeadersForDownload(fileName, httpStatus):
    response = f"\n{H1}{httpStatus}\n{HCT}{fileName}\n\n"
    return bytearray(response, 'utf-8')

class FileHandler:

    @staticmethod
    def openAndSend(fileName, connection):
        mutex.acquire()
        if (mutex.locked):
            connection.sendall(buildHeadersForDownload(fileName, OK))
            try:
                f = open(fileName,'rb')
                connection.sendfile(f)
                f.close()
            except:
                print('Erro ao abrir arquivo')
                f.close()
            mutex.release()
        else:
            print('Erro no mutex')
            return

def connectionEstablished(clientConnection):

    with clientConnection: # As it uses with statement, it's not necessary to call clientConnection.close()
        requestData = clientConnection.recv(4096).decode('utf-8')
        fileName = requestData[5:requestData.find("HTTP")-1]
        if fileName != 'favicon.ico':
            if fileName == '':
                message = 'Invalid URL. Please insert a path according to the following format\nlocalhost:' + str(PORT) + '/<file_name.ext>'
                clientConnection.sendall(buildErrorMessage(message, BAD_REQUEST))
                return
            if not path.isfile(fileName):
                message = 'File "' + fileName + '" not found in the root of the project'
                clientConnection.sendall(buildErrorMessage(message, BAD_REQUEST))
                return
            
            FileHandler.openAndSend(fileName, clientConnection)

if __name__ == "__main__":
    PORT = int(input("Which port? "))

    # TCP connection configuration. AF_INET refers to ipv4 and SOCK_STREAM is the TCP connection
    listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listenSocket.bind((HOST, PORT))
    listenSocket.listen(4096)
    print(f'Waiting for connections on port {PORT}')
    threads = list()

    while True:
        clientConnection, clientAddress = listenSocket.accept()
        thread = threading.Thread(target = connectionEstablished, args=(clientConnection, ))
        threads.append(thread)
        thread.start()
