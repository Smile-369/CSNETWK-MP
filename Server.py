import socket
import threading

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the host and port
HOST = 'localhost'
PORT = 5000

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

# Store a list of connected clients
clients = []

def handle_client(client_socket, address):
    """
    Handle incoming messages from a client.
    """
    while True:
        # Receive a message from the client
        message = client_socket.recv(1024).decode()

        # If the client disconnects, remove them from the list of clients and exit the loop
        if not message:
            clients.remove(client_socket)
            print(f'{address} disconnected.')
            break

        # Otherwise, send the message to all other connected clients
        for client in clients:
            if client != client_socket:
                client.sendall(message.encode())

def accept_clients():
    """
    Continuously accept incoming connections from clients.
    """
    while True:
        # Wait for a client to connect
        client_socket, address = server_socket.accept()

        # Add the client to the list of connected clients
        clients.append(client_socket)
        print(f'{address} connected.')

        # Start a new thread to handle incoming messages from the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

# Start accepting clients
accept_clients()