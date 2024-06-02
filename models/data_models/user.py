class User:
    def __init__(self, user_id, name, wallet):
        self.user_id = user_id
        self.name = name
        self.wallet = wallet

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "wallet": self.wallet,
        }
