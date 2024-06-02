import unittest
from models.data_models.user import User
from models.data_models.transaction import Transaction
from models.data_models.contract import SmartContract

class TestUserModel(unittest.TestCase):
    def test_user_creation(self):
        user = User(user_id=1, name="Wale Doe", wallet="0x456")
        self.assertEqual(user.user_id, 1)
        self.assertEqual(user.name, "Wale Doe")
        self.assertEqual(user.wallet, "0x456")

class TestTransactionModel(unittest.TestCase):
    def test_transaction_creation(self):
        transaction = Transaction(tx_id=1, from_address="0x123", to_address="0x456", value=100, gas=21000, gas_price=50, nonce=1)
        self.assertEqual(transaction.tx_id, 1)
        self.assertEqual(transaction.from_address, "0x123")
        self.assertEqual(transaction.to_address, "0x456")
        self.assertEqual(transaction.value, 100)
        self.assertEqual(transaction.gas, 21000)
        self.assertEqual(transaction.gas_price, 50)
        self.assertEqual(transaction.nonce, 1)

class TestSmartContractModel(unittest.TestCase):
    def test_smart_contract_creation(self):
        contract = SmartContract(contract_id=1, creator_address="0x123", contract_address="0x456")
        self.assertEqual(contract.contract_id, 1)
        self.assertEqual(contract.creator_address, "0x123")
        self.assertEqual(contract.contract_address, "0x456")

if __name__ == '__main__':
    unittest.main()
