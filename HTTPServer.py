import socket

# PORT < 1024 can require superuser permissions.
HOST, PORT = '127.0.0.1', 8080

def getFileName(requestData):
    refererIndex = requestData.find("Ref")
    if refererIndex != -1:
        referer = requestData[refererIndex:requestData.find("Accept-Encoding")]
        fileName = referer[referer.find("0/")+2:-2]
        return fileName
        
if __name__ == "__main__":
    # TCP connection configuration. AF_INET refers to ipv4 and SOCK_STREAM is the TCP connection
    listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listenSocket.bind((HOST, PORT))
    listenSocket.listen(1)
    print('Serving HTTP on port {PORT}...')

    while True:    
        clientConnection, clientAddress = listenSocket.accept()
        with clientConnection: # As it uses with statement, it's not necessary to call clientConnection.close()
            requestData = clientConnection.recv(1024).decode('utf-8')
            fileName = getFileName(requestData)
            if fileName != None:
                print(fileName)
            

            http_response = b"""\
HTTP/1.1 200 OK

Hello world
            """
            clientConnection.sendall(http_response)
