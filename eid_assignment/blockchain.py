import multichain
from datetime import datetime


class BlockchainConfig:
    def __init__(self):
        self.rpcuser = "multichainrpc"
        self.rpcpassword = "4Eaxwaw8HVn1cpNUDoCuHh695gwZcWWhiNtB4KN1miY4"
        self.rpchost = "127.0.0.1"
        self.rpcport = "9244"
        self.chainname = "test"
        self.stream_name = "FareContractStream"


# Blockchain Contract Manager
class BlockchainContractManager:
    def __init__(self, blockchain_config):
        self.config = blockchain_config
        self.mc = multichain.MultiChainClient(
            self.config.rpchost,
            self.config.rpcport,
            self.config.rpcuser,
            self.config.rpcpassword
        )
        self.ensure_stream_exists()

    def ensure_stream_exists(self):
        streams = self.mc.liststreams()
        stream_names = [stream['name'] for stream in streams] if streams else []

        if self.config.stream_name not in stream_names:
            try:
                txid = self.mc.create('stream', self.config.stream_name, True)
                print(f"Created stream {self.config.stream_name}, txid: {txid}")
                self.mc.subscribe(['stream', self.config.stream_name])
                print(f"Subscribed to stream {self.config.stream_name}")
            except Exception as e:
                print(f"Error creating stream: {e}")

    def deploy_contract(self, contract_code, version):
        contract_data = {
            "json": {
                "code": contract_code,
                "version": version,
                "timestamp": datetime.now().isoformat()
            }
        }
        key = f"contract-v{version}"
        try:
            txid = self.mc.publish(self.config.stream_name, key, contract_data)
            print(f"Deployed contract version {version}, txid: {txid}")
            return txid
        except Exception as e:
            print(f"Error deploying contract: {e}")
            return None

    def get_latest_contract(self):
        try:
            items = self.mc.liststreamitems(self.config.stream_name)
            if items:
                contract_items = [item for item in items if item['keys'][0].startswith('contract-v')]
                if contract_items:
                    contract_items.sort(key=lambda x: int(x['keys'][0].split('-v')[1]), reverse=True)
                    latest = contract_items[0]
                    return latest['data']['json']
            return None
        except Exception as e:
            print(f"Error retrieving latest contract: {e}")
            return None


class SmartContractTemplate:
    def __init__(self):
        self.template = """
class FareContract:
    def __init__(self, base_fare=10.0):
        self.base_fare = base_fare
        self.discount_threshold = 500
        self.discount_percentage = 0.0
        self.last_updated = "{timestamp}"

    def calculate_fare(self, passenger_count):
        fare = self.base_fare
        if passenger_count < self.discount_threshold:
            fare = self.base_fare * (1 - self.discount_percentage)
        return fare

    def get_contract_details(self):
        return {{
            "base_fare": self.base_fare,
            "discount_threshold": self.discount_threshold,
            "discount_percentage": self.discount_percentage,
            "last_updated": self.last_updated
        }}
"""

    def get_current_template(self):
        return self.template.format(timestamp=datetime.now().isoformat())
