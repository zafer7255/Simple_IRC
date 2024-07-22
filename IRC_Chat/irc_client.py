import socket
import threading

class IRCClient:
    def __init__(self, host, port, nickname):
        self.host = host
        self.port = port
        self.nickname = nickname
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.client.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}")

        # Receive the prompt to choose a room
        prompt = self.client.recv(1024).decode("utf-8")
        print(prompt, end="")
        
        # Choose a room and send it to the server
        room = input()
        self.client.sendall(room.encode("utf-8"))

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        while True:
            message = input()
            self.send_message(message)

    def send_message(self, message):
        full_message = f"{self.nickname}: {message}"
        self.client.sendall(full_message.encode("utf-8"))

    def receive_messages(self):
        while True:
            try:
                data = self.client.recv(1024)
                if not data:
                    break

                message = data.decode("utf-8")
                print(message)

            except ConnectionResetError:
                print("Server closed the connection.")
                break

if __name__ == "__main__":
    nickname = input("Enter your nickname: ")
    client = IRCClient("127.0.0.1", 6666, nickname)
    client.start()
