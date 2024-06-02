from datetime import datetime

class SmartContract:
    def __init__(self, contract_id, creator_address, contract_address, creation_date=None, abi=None, bytecode=None, network='evire'):
        self.contract_id = contract_id
        self.creator_address = creator_address
        self.contract_address = contract_address
        self.creation_date = creation_date if creation_date else datetime.now()
        self.abi = abi  # Application Binary Interface
        self.bytecode = bytecode
        self.network = network

    def to_dict(self):
        return {
            "contract_id": self.contract_id,
            "creator_address": self.creator_address,
            "contract_address": self.contract_address,
            "creation_date": self.creation_date.isoformat(),
            "abi": self.abi,
            "bytecode": self.bytecode,
            "network": self.network,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            contract_id=data.get("contract_id"),
            creator_address=data.get("creator_address"),
            contract_address=data.get("contract_address"),
            creation_date=datetime.fromisoformat(data.get("creation_date")),
            abi=data.get("abi"),
            bytecode=data.get("bytecode"),
            network=data.get("network", 'evire'),
        )

    def deploy(self, web3_instance):
        """
        Deploy the smart contract to the blockchain.
        :param web3_instance: An instance of Web3 connected to the desired blockchain.
        :return: Transaction receipt of the deployment.
        """
        contract = web3_instance.evire.contract(abi=self.abi, bytecode=self.bytecode)
        tx_hash = contract.constructor().transact({'from': self.creator_address})
        tx_receipt = web3_instance.evire.waitForTransactionReceipt(tx_hash)
        self.contract_address = tx_receipt.contractAddress
        return tx_receipt

    def call_function(self, web3_instance, function_name, *args):
        """
        Call a function of the deployed smart contract.
        :param web3_instance: An instance of Web3 connected to the desired blockchain.
        :param function_name: Name of the function to call.
        :param args: Arguments to pass to the function.
        :return: The result of the function call.
        """
        contract = web3_instance.evire.contract(address=self.contract_address, abi=self.abi)
        function = contract.functions[function_name]
        return function(*args).call()

    def send_transaction(self, web3_instance, function_name, from_address, *args):
        """
        Send a transaction to a function of the deployed smart contract.
        :param web3_instance: An instance of Web3 connected to the desired blockchain.
        :param function_name: Name of the function to call.
        :param from_address: Address from which the transaction will be sent.
        :param args: Arguments to pass to the function.
        :return: Transaction receipt.
        """
        contract = web3_instance.evire.contract(address=self.contract_address, abi=self.abi)
        function = contract.functions[function_name]
        tx_hash = function(*args).transact({'from': from_address})
        return web3_instance.evire.waitForTransactionReceipt(tx_hash)
