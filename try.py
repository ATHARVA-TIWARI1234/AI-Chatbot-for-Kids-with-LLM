import socket

def send_file(filename, host='localhost', port=65432):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to all IP addresses of this host and a port
    s.bind((host, port))
    # Enable the server to accept connections (make it a listening socket)
    s.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        # Accept a connection from a client
        client_socket, addr = s.accept()
        print('Got a connection from', addr)
        # Open the file to be sent
        with open(filename, 'rb') as f:
            # Read the file content
            data = f.read()
            # Send the file content to the client
            client_socket.sendall(data)

        # Close the client socket
        client_socket.close()
        print("File has been sent and socket is closed.")

        # End the loop after sending the file
        break

    # Close the server socket
    s.close()

# Example usage: send_file('sample.txt')
send_file('output.txt')