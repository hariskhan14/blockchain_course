import socket
import hashlib
import rsa


def generate_md5(input_string):
    return hashlib.md5(input_string.encode()).hexdigest()


def start_client():
    host = '127.0.0.1'
    port_server = 55442
    port_client_b = 55444

    client_socket_a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket_a.connect((host, port_server))
    print(f"Connected to server at {host}:{port_server}")

    client_socket_b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket_b.connect((host, port_client_b))
    print(f"Connected to server 2 at {host}:{port_client_b}")

    my_hash = generate_md5("Ghoofy")
    with open("public.pem", "rb") as pub_file:
        public_key = rsa.PublicKey.load_pkcs1(pub_file.read())

    while True:
        input_message = input("Enter message to send to server (or 'quit' to exit): ")
        message = input_message + ":" + my_hash
        if message.lower() == 'quit':
            break

        enc_message = rsa.encrypt(message.encode(),
                                  public_key)

        client_socket_a.sendall(enc_message)
        client_socket_b.sendall(enc_message)

    client_socket_a.close()
    client_socket_b.close()


if __name__ == "__main__":
    start_client()
