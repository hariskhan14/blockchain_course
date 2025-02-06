import socket

class Node:
    value: str
    hash: str
    next
    
    def __init__(self, value, hash):
        self.value = value
        self.hash = hash
        self.next = None

class LinkedList:
    head: Node
    def __init__(self):
        self.head = None

    def add(self, data, hash):
        newNode = Node(data, hash)
        if self.head is None:
            self.head = newNode
            return
        
        curr = self.head
        while(curr.next is not None):
            curr = curr.next
        
        curr.next = newNode
    
    def print(self, hash):
        curr = self.head
        while(curr is not None):
            if curr.hash == hash:
                print(curr.value)
            curr = curr.next

def start_server():
    host = '127.0.0.1' 
    port = 55442

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    blockchain = LinkedList()


    while True:
        connection, client_address = server_socket.accept()
        print(f"Connected by {client_address}")

        while True:
            data = connection.recv(1024)
            if not data:
                break

            msg_received = data.decode().split(";")

            print(f"Received from client: {msg_received}")

            if(msg_received[0] == 'print'):
                blockchain.print(msg_received[1])
            else:
                blockchain.add(msg_received[0], msg_received[1])

            
        connection.close()

if __name__ == "__main__":
    start_server()