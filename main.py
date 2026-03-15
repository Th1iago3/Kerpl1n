import socket
import threading
import os

# Define the host and port for the server
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 8080        # Port to listen on

# Function to handle client requests
def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    print(request)  # Print the received request for debugging

    # Parse the request and serve files accordingly
    try:
        # Get the requested file from the HTTP GET request
        filename = request.split(' ')[1][1:]  # Strip the leading '/'
        
        if filename == '':
            filename = 'index.html'  # Default to index.html if no file specified
        
        # Check if the file exists
        if os.path.isfile(filename):
            with open(filename, 'rb') as f:
                response_body = f.read()
            response_header = 'HTTP/1.1 200 OK\n\n'
        else:
            response_body = b'404 Not Found'
            response_header = 'HTTP/1.1 404 Not Found\n\n'
        
        # Send the response back to the client
        client_socket.sendall(response_header.encode('utf-8') + response_body)
    
    except Exception as e:
        print(f"Error: {e}")
        client_socket.sendall(b'HTTP/1.1 500 Internal Server Error\n\n')
    
    finally:
        client_socket.close()

# Main server loop
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f'Server is listening on http://{HOST}:{PORT}/')

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f'Accepted connection from {addr}')
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except KeyboardInterrupt:
        print('Shutting down the server...')
    finally:
        server_socket.close()

# Start the server
if __name__ == '__main__':
    start_server()