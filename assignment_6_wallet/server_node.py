import socket
import json
import threading
import time
import multichain

RPC_USER = "multichainrpc"
RPC_PASSWORD = "EAfvghj8yr1tcpNUDoCuHh695gwZcWWhiNtB4KN1miY4"
RPC_HOST = "127.0.0.1"
RPC_PORT = "9244"
CHAIN_NAME = "mychain1"
mc = multichain.MultiChainClient(RPC_HOST, RPC_PORT, RPC_USER, RPC_PASSWORD)

full_ledger = []
global_ledger = []

STREAM_NAME = "mystream123"


def setup_stream():
    mc.create('stream', STREAM_NAME, True)

    print(f"Subscribing to stream: {STREAM_NAME}")
    mc.subscribe(['stream', STREAM_NAME])


def process_transaction(sender, receiver, asset, amount):
    try:
        txid = mc.publish(STREAM_NAME, receiver, {'json': {'Coinname': asset, 'amount': amount}})

        transaction = {
            "txid": txid,
            "sender": sender,
            "receiver": receiver,
            "asset": asset,
            "amount": amount,
            "timestamp": time.time()
        }
        full_ledger.append(transaction)

        global_ledger.append({
            "txid": txid,
            "sender": sender,
            "receiver": receiver,
            "asset": asset,
            "amount": amount,
            "timestamp": transaction["timestamp"]
        })
        return {"status": "success", "txid": txid}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def handle_client(conn, addr):
    print(f"Connection from {addr}")

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            request = json.loads(data)

            if request["type"] == "transaction":
                response = process_transaction(request["sender"], request["receiver"], request["asset"],
                                               request["amount"])
            elif request["type"] == "get_ledger":
                response = {"global_ledger": global_ledger}
            else:
                response = {"status": "error", "message": "Invalid request type"}

            conn.send(json.dumps(response).encode())
        except Exception as e:
            print(f"Error: {e}")
            break
    conn.close()


def start_server():
    print(f"Setting up stream {STREAM_NAME}")
    setup_stream()

    host = "127.0.0.1"
    port = 65432

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"Server started on {host}:{port}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()


if __name__ == "__main__":
    start_server()
