import socket
import json

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 65432


def send_request(request):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_HOST, SERVER_PORT))

        client.send(json.dumps(request).encode())
        response = json.loads(client.recv(4096).decode())

        client.close()
        return response
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    while True:
        print("1: Send a Transaction")
        print("2: Get Global Ledger")
        choice = input("Enter choice: ")

        if choice == "1":
            sender = input("Sender: ")
            receiver = input("Receiver: ")
            asset = input("Asset: ")
            amount = float(input("Amount: "))

            request = {
                "type": "transaction",
                "sender": sender,
                "receiver": receiver,
                "asset": asset,
                "amount": amount
            }
            result = send_request(request)
            print("Transaction Result:", result)

        elif choice == "2":
            request = {"type": "get_ledger"}
            ledger = send_request(request)
            print("Global Ledger:", json.dumps(ledger, indent=4))

        else:
            print("Invalid Choice!")
