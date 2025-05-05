import hashlib
import json
import time


# Confidentiality

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp or int(time.time())
        self.transactions = transactions
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_data = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_data.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", [], int(time.time()))
        self.chain.append(genesis_block)

    def add_block(self, transactions):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), previous_block.hash, transactions)
        new_block.hash = new_block.compute_hash()
        self.chain.append(new_block)

    def verify_chain(self):
        for i in range(1, len(self.chain)):
            if self.chain[i].previous_hash != self.chain[i - 1].hash:
                return False
        return True


# Example Usage
blockchain = Blockchain()
blockchain.add_block([{"patient_id": "abc123", "record_hash": "xyz789"}])

print(json.dumps(blockchain.chain, indent=4))
