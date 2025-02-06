import rsa
import socket
import hashlib
import random


def generate_md5(input_string):
    return hashlib.md5(input_string.encode()).hexdigest()


def start_client():
    host = '127.0.0.1'
    port = 55442

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    my_hash = generate_md5("Ghoofy")

    # random.seed(42)
    # publicKey, privateKey = rsa.newkeys(512)
    # print(privateKey)
    with open("public.pem", "rb") as pub_file:
        public_key = rsa.PublicKey.load_pkcs1(pub_file.read())
    while True:
        input_message = input("Enter message to send to server (or 'quit' to exit): ")
        message = input_message + ":" + my_hash
        if message.lower() == 'quit':
            break

        enc_message = rsa.encrypt(message.encode(), public_key)
        client_socket.sendall(enc_message)

    client_socket.close()


if __name__ == "__main__":
    start_client()
