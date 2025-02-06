import socket

def start_client():
    host = '127.0.0.1'
    port = 55442

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    while True:
        message = input("Enter message to send to server (or 'quit' to exit): ")

        if message.lower() == 'quit':
            break
        client_socket.sendall(message.encode())

    client_socket.close()

if __name__ == "__main__":
    start_client()