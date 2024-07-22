import socket
import threading

class IRCServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []  # List to keep track of connected clients
        self.rooms = {}  # Dictionary to store clients in each room

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen()

        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_handler.start()

    def handle_client(self, client_socket, client_address):
        print(f"New connection from {client_address}")
        
        # Prompt the client to choose a room
        client_socket.sendall("Choose a room: ".encode("utf-8"))
        room = client_socket.recv(1024).decode("utf-8").strip()
        
        # Add the client to the chosen room
        self.rooms.setdefault(room, []).append(client_socket)

        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break

                message = data.decode("utf-8")
                print(f"Received from {client_address} in room {room}: {message}")

                # Broadcast the message to all clients in the same room
                self.broadcast(message, client_socket, room)

        except ConnectionResetError:
            pass  # Handle client disconnect

        finally:
            print(f"Connection closed by {client_address}")
            # Remove the client from the room
            if room in self.rooms:
                self.rooms[room].remove(client_socket)
            client_socket.close()

    def broadcast(self, message, sender_socket, room):
        # Broadcast the message to all clients in the same room
        if room in self.rooms:
            for client in self.rooms[room]:
                if client != sender_socket:
                    try:
                        client.sendall(message.encode("utf-8") + b'\n')  # Add a newline character to each message
                    except BrokenPipeError:
                        continue

if __name__ == "__main__":
    server = IRCServer("127.0.0.1", 6666)
    server.start()