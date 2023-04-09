import socket
import threading
import tkinter as tk

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the host and port
HOST = ''
PORT = 5000


class ChatWindow(tk.Tk):
    """
    The main chat window.
    """

    def __init__(self):
        super().__init__()

        # Set the window title
        self.title('Chat')

        # Create the chat history display
        self.chat_history = tk.Text(self, state=tk.DISABLED)
        self.chat_history.pack(expand=True, fill=tk.BOTH)

        # Create the message input field
        self.message_entry = tk.Entry(self)
        self.message_entry.pack(side=tk.BOTTOM, fill=tk.X)

        # Bind the enter key to the send_message function
        self.message_entry.bind('<Return>', self.send_message)

        # Connect to the server
        self.connect()

    def connect(self):
        """
        Connect to the server.
        """
        # Display a message prompting the user to connect
        self.add_message('To connect, type "/join (ip address) (port)" and press Enter.\n')

    def send_message(self, event=None):
        """
        Send a message to the server.
        """
        # Get the message from the input field
        message = self.message_entry.get()

        # Clear the input field
        self.message_entry.delete(0, tk.END)

        # Check if the socket is connected
        if not client_socket._closed:
            # Send the message to the server
            client_socket.sendall(message.encode())

            # Add the message to the chat history
            self.add_message(f'You: {message}\n')
        else:
            # Display an error message if the socket is not connected
            self.add_message('Not connected.\n')

    def add_message(self, message):
        """
        Add a message to the chat history.
        """
        # Enable the chat history so we can modify it
        self.chat_history.config(state=tk.NORMAL)

        # Add the message to the chat history
        self.chat_history.insert(tk.END, message)

        # Disable the chat history again so the user can't modify it
        self.chat_history.config(state=tk.DISABLED)


class Client:
    """
    The chat client.
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        """
        Connect to the server.
        """
        try:
            # Create a connection to the server
            client_socket.connect((self.host, self.port))

            # Start a new thread to handle incoming messages from the server
            server_thread = threading.Thread(target=self.handle_server_messages)
            server_thread.start()

        except socket.error as e:
            # Display an error message if the connection fails
            chat_window.add_message(f'Error connecting to server: {e}\n')

    def handle_server_messages(self):
        """
        Handle incoming messages from the server.
        """
        while True:
            try:
                # Receive a message from the server
                message = client_socket.recv(1024).decode()

                # Add the message to the chat history
                chat_window.add_message(message)

            except socket.error as e:
                # Display an error message if the connection was lost
                chat_window.add_message(f'Error receiving message: {e}\n')
                break

        # Close the socket when the connection is lost
        client_socket.close()


# Create the main chat window
chat_window = ChatWindow()


# Define the /join command
def join_command(args):
    """
    Handle the /join command.
    """
    # Parse the IP address and port from the arguments
    try:
        address, port = args.split()

        # Create a new client and connect to the server
        client.host = address
        client.port = int(port)
        client.connect()

        # Display a message indicating that we've connected to the new server
        chat_window.add_message(f'Connected to {address}:{port}\n')

    except:
        # Display an error message if the command is invalid
        chat_window.add_message(f'Invalid command: {command}\n')


# Start the main event loop
chat_window.mainloop()
