from logging import exception
import socket

# PORT < 1024 can require superuser permissions.
HOST, PORT = '', 8080

H1 = 'HTTP/1.1 200 OK'
HCT = 'Content-Disposition: attachment; filename='

def buildErrorMessage(message):
    response = f"\n{H1}\n\n{message}\n"
    return bytearray(response, 'utf-8')

def buildHeadersForDownload(fileName):
    response = f"\n{H1}\n{HCT}{fileName}\n\n"
    return bytearray(response, 'utf-8')

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
                    message = 'Invalid URL. Please insert a path according to the following format\nlocalhost:' + str(PORT) + '/<file_name.ext>'
                    clientConnection.sendall(buildErrorMessage(message))
                    continue
                try:
                    file = open(fileName, 'rb')
                    fileSize = len(file.read())
                    file.close()
                    clientConnection.sendall(buildHeadersForDownload(fileName))

                    f = open(fileName,'rb')
                    content = f.read()
                    clientConnection.sendall(content)

                except FileNotFoundError:
                    message = 'File "' + fileName + '" not found in the root of the project'
                    clientConnection.sendall(buildErrorMessage(message))
