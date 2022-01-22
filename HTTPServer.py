import socket
import threading

# PORT < 1024 can require superuser permissions.
HOST, PORT = '', 8081

H1 = 'HTTP/1.1 200 OK'
HCT = 'Content-Disposition: attachment; filename='

def buildErrorMessage(message):
    response = f"\n{H1}\n\n{message}\n"
    return bytearray(response, 'utf-8')

def buildHeadersForDownload(fileName):
    response = f"\n{H1}\n{HCT}{fileName}\n\n"
    return bytearray(response, 'utf-8')

class FileHandler:

    def __init__(self, connection):
        self._lock = threading.Lock() #Start mutex opened
        self.connection = connection

    def openAndSend(self, fileName):
        try:
            with self._lock: # Lock, and in the end of the with statement, opens again
                print('Thread locked file')
                f = open(fileName,'rb')
                content = f.read()
                f.close()
            print('Thread released file')
            self.connection.sendall(buildHeadersForDownload(fileName))
            self.connection.sendall(content)

        except FileNotFoundError:
            message = 'File "' + fileName + '" not found in the root of the project'
            self.connection.sendall(buildErrorMessage(message))

def connectionEstablished(clientConnection):

    with clientConnection: # As it uses with statement, it's not necessary to call clientConnection.close()
        requestData = clientConnection.recv(4096).decode('utf-8')
        fileName = requestData[5:requestData.find("HTTP/1.1")-1]
        if fileName != 'favicon.ico':
            print('valid thread starting')
            if fileName == '':
                message = 'Invalid URL. Please insert a path according to the following format\nlocalhost:' + str(PORT) + '/<file_name.ext>'
                clientConnection.sendall(buildErrorMessage(message))
                return
            
            fileHandler = FileHandler(clientConnection)
            fileHandler.openAndSend(fileName)

if __name__ == "__main__":

    # TCP connection configuration. AF_INET refers to ipv4 and SOCK_STREAM is the TCP connection
    listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listenSocket.bind((HOST, PORT))
    listenSocket.listen(5)
    print('Serving HTTP on port ' + str(PORT))
    threads = list()

    while True:
        clientConnection, clientAddress = listenSocket.accept()
        thread = threading.Thread(target = connectionEstablished, args=(clientConnection,))
        threads.append(thread)
        thread.start()
