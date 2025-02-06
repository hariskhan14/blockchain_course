import socket
import hashlib


def start_server():
    host = '127.0.0.1'
    port = 55442

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    salt = 'hello-world'
    ledger = [
    ]

    while True:
        connection, client_address = server_socket.accept()
        print(f"Connected by {client_address}")

        while True:
            data = connection.recv(1024)
            if not data:
                break

            msg_received = data.decode()

            print(f"Received from client: {msg_received}")

            if msg_received == 'print':
                print_data(ledger)
                continue

            if msg_received.startswith('change'):
                msgs = msg_received.split(',')
                idx = int(msgs[1])
                data = msgs[2]

                new_hash = get_md5_of_string(data)
                if new_hash == ledger[idx + 1]['previous']:
                    ledger[idx]['message'] = data
                else:
                    print("Data tampered")
                    print(f'received: {data}, actual: {ledger[idx]['message']}.')
                continue

            if len(ledger) == 0:
                ledger.append({
                    'previous': get_md5_of_string(salt),
                    'message': str(msg_received),
                })
            else:
                ledger.append({
                    'previous': get_md5_of_string(ledger[len(ledger) - 1]['message']),
                    'message': str(msg_received),
                })

        connection.close()


def get_md5_of_string(input_string):
    return hashlib.md5(input_string.encode()).hexdigest()


def print_data(ledger):
    for data in ledger:
        print(data)


if __name__ == "__main__":
    start_server()