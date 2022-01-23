import socket
import threading
import resource

# PORT < 1024 can require superuser permissions.
HOST, PORT = '', 8080

H1 = 'HTTP/1.1 '
HCT = 'Content-Disposition: attachment; filename='

NOT_FOUND = '404 Not Found'
BAD_REQUEST = '400 Bad Request'
OK = '200 OK'

resource.setrlimit(resource.RLIMIT_NOFILE, (4200, 4200))
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
        try:
            mutex.acquire()
            with open(fileName,'rb') as f:
                connection.sendall(buildHeadersForDownload(fileName, OK))
                connection.sendfile(f)
            mutex.release()
            print('thread finished with success')

        except FileNotFoundError:
            message = 'File "' + fileName + '" not found in the root of the project'
            connection.sendall(buildErrorMessage(message, NOT_FOUND))
            mutex.release()
            print('thread finished with not found')

def connectionEstablished(clientConnection):

    with clientConnection: # As it uses with statement, it's not necessary to call clientConnection.close()
        requestData = clientConnection.recv(4096).decode('utf-8')
        fileName = requestData[5:requestData.find("HTTP")-1]
        if fileName != 'favicon.ico':
            if fileName == '':
                message = 'Invalid URL. Please insert a path according to the following format\nlocalhost:' + str(PORT) + '/<file_name.ext>'
                clientConnection.sendall(buildErrorMessage(message, BAD_REQUEST))
                return
            
            FileHandler.openAndSend(fileName, clientConnection)

if __name__ == "__main__":

    # TCP connection configuration. AF_INET refers to ipv4 and SOCK_STREAM is the TCP connection
    listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listenSocket.bind((HOST, PORT))
    listenSocket.listen(4096)
    threads = list()

    while True:
        clientConnection, clientAddress = listenSocket.accept()
        thread = threading.Thread(target = connectionEstablished, args=(clientConnection, ))
        threads.append(thread)
        thread.start()
