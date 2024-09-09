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

    def get_user_id(self):
        return self.user_id

class SavingsAccount(Account):
    def __init__(self, user_id, name, pin, balance=0, interest_rate=0.02):
        super().__init__(user_id, name, pin, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        self.balance += self.balance * self.interest_rate
        print(f"Odsetki zostały dodane. Nowe saldo: {self.balance}")

class CheckingAccount(Account):
    def __init__(self, user_id, name, pin, balance=0, transaction_fee=1.0):
        super().__init__(user_id, name, pin, balance)
        self.transaction_fee = transaction_fee

    def withdraw(self, amount):
        total_amount = amount + self.transaction_fee
        if self.balance >= total_amount:
            self.balance -= total_amount
            print(f"Opłata transakcyjna: {self.transaction_fee} zł. Wypłata zrealizowana.")
            return True
        print("Brak wystarczających środków na koncie.")
        return False