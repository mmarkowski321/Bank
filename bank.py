class Account:
    def __init__(self, user_id, name, pin, balance=0):
        self.user_id = user_id
        self.name = name
        self.pin = pin
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False

    def get_balance(self):
        return self.balance
