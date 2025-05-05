import os
import json
import time
import numpy as np
import pandas as pd
from datetime import datetime

import blockchain
import aimodel
import google.generativeai as genai


class PassengerDataSimulator:
    def __init__(self):
        self.daily_passengers = np.random.randint(300, 700)
        self.trend = 0

    def get_passenger_data(self):
        if np.random.random() < 0.3:
            self.trend = np.random.choice([-1, 0, 1])
        change = np.random.randint(0, 50) * self.trend
        self.daily_passengers = max(50, self.daily_passengers + change)

        return {
            "timestamp": datetime.now().isoformat(),
            "passenger_count": self.daily_passengers,
            "day_of_week": datetime.now().strftime("%A"),
            "time_of_day": datetime.now().strftime("%H:%M")
        }


class SmartFareSystem:
    def __init__(self):
        self.blockchain_config = blockchain.BlockchainConfig()
        self.ai_config = aimodel.AIConfig()
        self.template_manager = blockchain.SmartContractTemplate()
        self.passenger_simulator = PassengerDataSimulator()
        self.ai_modifier = aimodel.AIContractModifier(self.ai_config)
        self.blockchain_manager = blockchain.BlockchainContractManager(self.blockchain_config)
        self.current_version = 0

    def initialize_system(self):
        latest_contract = self.blockchain_manager.get_latest_contract()
        if latest_contract:
            print("Found existing contract on blockchain")
            self.current_contract_code = latest_contract['code']
            self.current_version = latest_contract['version']
        else:
            print("No existing contract found, deploying initial version")
            self.current_contract_code = self.template_manager.get_current_template()
            self.current_version = 1
            self.blockchain_manager.deploy_contract(self.current_contract_code, self.current_version)

    def evaluate_conditions(self, passenger_data):
        if "discount_percentage = " in self.current_contract_code:
            try:
                current_discount = float(self.current_contract_code.split("discount_percentage = ")[1].split("\n")[0])
            except:
                current_discount = 0.0
        else:
            current_discount = 0.0

        passenger_count = passenger_data['passenger_count']

        if passenger_count >= 500 and current_discount > 0:
            return True
        elif passenger_count < 300 and current_discount != 0.3:
            return True
        elif 300 <= passenger_count < 400 and current_discount != 0.2:
            return True
        elif 400 <= passenger_count < 500 and current_discount != 0.1:
            return True

        return False

    def run_cycle(self):
        passenger_data = self.passenger_simulator.get_passenger_data()
        print(f"\nCurrent passenger count: {passenger_data['passenger_count']}")

        if self.evaluate_conditions(passenger_data):
            print("Conditions met for contract update")
            modified_contract = self.ai_modifier.modify_contract(
                self.current_contract_code,
                passenger_data
            )
            self.current_version += 1
            txid = self.blockchain_manager.deploy_contract(modified_contract, self.current_version)

            if txid:
                self.current_contract_code = modified_contract
                print(f"Contract updated and deployed as version {self.current_version}")

                if "discount_percentage = " in self.current_contract_code:
                    try:
                        discount = float(self.current_contract_code.split("discount_percentage = ")[1].split("\n")[0])
                        print(f"New fare discount: {discount * 100:.1f}%")
                    except:
                        pass
            else:
                print("Failed to deploy updated contract")
        else:
            print("No contract update needed at this time")

    def start(self):
        print("Initializing Dynamic Fare Adjustment System...")
        self.initialize_system()

        cycles = 5
        print(f"\nRunning system for {cycles} cycles ")

        for cycle in range(1, cycles + 1):
            print(f"\nCycle {cycle}")
            self.run_cycle()
            if cycle < cycles:
                time.sleep(5)

        print("\nSystem execution completed")


# Run the system
if __name__ == "__main__":
    system = SmartFareSystem()
    system.start()
