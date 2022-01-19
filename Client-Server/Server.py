import socket

# Empty string HOST will be able to connect to all available ipv4 interfaces. Run 'netstat -an' in the terminal
# after running script to see the difference of the connection established when using 0.0.0.0 
HOST, PORT = '', 8080

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
        listen_socket.bind((HOST, PORT))
        listen_socket.listen()
        connection, address = listen_socket.accept() # Accept blocks and waits for a client connection
        with connection:
            print('Connected by', address)
            while True:
                data = connection.recv(1024)
                # Reads the data that client sent
                if not data: # recv returns empty bytes if client closes connection
                    break
                connection.sendall(data) # Send the data that the client sent 