import socket
import hashlib
from cryptography.fernet import Fernet
import base64


def generate_md5(input_string):
    return hashlib.md5(input_string.encode()).hexdigest()


def start_client():
    host = '127.0.0.1'
    port = 55442

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    my_signature = generate_md5("haris-salt")
    my_key = Fernet(b'0S1X4E1D0prpiAQp0NPPL_Ce7t-d3V4HvsZ7oCMPRM4=')

    while True:
        message = input("Name: ")
        birthday = input("Birthday: ")
        nic = input("Nic: ")
        phone = input("Phone: ")
        blood_type = input("Blood type: ")
        gender = input("Gender: ")

        final_msg = message + ';' + birthday + ';' + nic + ';' + phone + ';' + blood_type + ';' + gender

        signed_msg = my_key.encrypt(final_msg.encode())

        client_socket.sendall(signed_msg)

    # client_socket.close()


if __name__ == "__main__":
    start_client()