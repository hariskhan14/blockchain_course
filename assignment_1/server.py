import socket
import hashlib
from cryptography.fernet import Fernet

def generate_md5(input_string):
    return hashlib.md5(input_string.encode()).hexdigest()

def start_server():
    host = '127.0.0.1' 
    port = 55442
    
    my_key = Fernet(b'0S1X4E1D0prpiAQp0NPPL_Ce7t-d3V4HvsZ7oCMPRM4=')
    client_signature = generate_md5("haris-salt")  
    server_signature = generate_md5("haris-salt")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    while True:
        connection, client_address = server_socket.accept()
        print(f"Connected by {client_address}")

        while True:
            data = connection.recv(1024)
            if not data:
                break

            msg_received = data.decode()
            
            print(f"Received from client: {msg_received}")
            
            dec = my_key.decrypt(msg_received) 
            
            print(f'decrypted: {dec}')
            
            msg, sign = dec.split(",")
            
            if generate_md5(msg) != sign:
                print("Invalid data") 
                continue
            
            print('Now adding my signature')
            
            print(f"data: {msg}: my_sign: {server_signature}")    
            
        connection.close()
    
    
if __name__ == "__main__":
    start_server()