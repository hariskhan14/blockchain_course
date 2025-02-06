import socket
import hashlib
import rsa


def generate_md5(input_string):
    return hashlib.md5(input_string.encode()).hexdigest()


def start_server():
    host = '127.0.0.1'
    port = 55442

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    server_socket.listen(2)
    print(f"Server listening on {host}:{port}")

    my_hash = generate_md5("Alice")
    with open("private.pem", "rb") as priv_file:
        private_key = rsa.PrivateKey.load_pkcs1(priv_file.read())

    while True:
        connection, client_address = server_socket.accept()
        print(f"Connected by {client_address}")

        while True:
            data = connection.recv(1024)
            if not data:
                break

            dec_message = rsa.decrypt(data, private_key).decode()

            print(f"Received from client: {dec_message}")

            message, receiver = dec_message.split(":")

            my_message = message + ":" + my_hash

            print(f"Received after adding alice signature client: {my_message}")

        connection.close()


if __name__ == "__main__":
    start_server()
