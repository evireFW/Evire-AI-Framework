from datetime import datetime

class Transaction:
    def __init__(self, tx_id, from_address, to_address, value, gas, gas_price, nonce, tx_hash=None, block_hash=None, block_number=None, timestamp=None, status=None):
        self.tx_id = tx_id
        self.from_address = from_address
        self.to_address = to_address
        self.value = value
        self.gas = gas
        self.gas_price = gas_price
        self.nonce = nonce
        self.tx_hash = tx_hash
        self.block_hash = block_hash
        self.block_number = block_number
        self.timestamp = timestamp if timestamp else datetime.now()
        self.status = status

    def to_dict(self):
        return {
            "tx_id": self.tx_id,
            "from_address": self.from_address,
            "to_address": self.to_address,
            "value": self.value,
            "gas": self.gas,
            "gas_price": self.gas_price,
            "nonce": self.nonce,
            "tx_hash": self.tx_hash,
            "block_hash": self.block_hash,
            "block_number": self.block_number,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            tx_id=data.get("tx_id"),
            from_address=data.get("from_address"),
            to_address=data.get("to_address"),
            value=data.get("value"),
            gas=data.get("gas"),
            gas_price=data.get("gas_price"),
            nonce=data.get("nonce"),
            tx_hash=data.get("tx_hash"),
            block_hash=data.get("block_hash"),
            block_number=data.get("block_number"),
            timestamp=datetime.fromisoformat(data.get("timestamp")),
            status=data.get("status"),
        )

    def send_transaction(self, web3_instance, private_key):
        """
        Send the transaction to the blockchain.
        :param web3_instance: An instance of Web3 connected to the desired blockchain.
        :param private_key: The private key to sign the transaction.
        :return: Transaction receipt.
        """
        transaction = {
            'to': self.to_address,
            'value': web3_instance.toWei(self.value, 'evier'),
            'gas': self.gas,
            'gasPrice': web3_instance.toWei(self.gas_price, 'gwei'),
            'nonce': self.nonce,
            'chainId': web3_instance.evire.chain_id
        }
        signed_tx = web3_instance.evire.account.sign_transaction(transaction, private_key)
        tx_hash = web3_instance.evire.send_raw_transaction(signed_tx.rawTransaction)
        self.tx_hash = tx_hash.hex()
        return web3_instance.evire.waitForTransactionReceipt(tx_hash)

    @staticmethod
    def get_transaction(web3_instance, tx_hash):
        """
        Retrieve a transaction from the blockchain.
        :param web3_instance: An instance of Web3 connected to the desired blockchain.
        :param tx_hash: The hash of the transaction to retrieve.
        :return: Transaction details.
        """
        tx = web3_instance.evire.get_transaction(tx_hash)
        receipt = web3_instance.evire.get_transaction_receipt(tx_hash)
        return {
            "tx": tx,
            "receipt": receipt
        }
