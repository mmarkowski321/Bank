class Account:
    def __init__(self, user_id, name, pin, balance=0):
        self.user_id = user_id
        self.name = name
        self.pin = pin
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return {"message": f"Wpłacono {amount}. Nowe saldo: {self.balance}"}
        return {"error": "Kwota musi być większa od zera."}

    def withdraw(self, amount):
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                return {"message": f"Wypłacono {amount}. Nowe saldo: {self.balance}"}
            return {"error": "Niewystarczające środki na koncie."}
        return {"error": "Kwota musi być większa od zera."}

    def get_balance(self):
        return {"user_id": self.user_id, "balance": self.balance}

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "balance": self.balance,
            "type": self.__class__.__name__
        }


class RegularAccount(Account):
    def __init__(self, user_id, name, pin, balance=0):
        super().__init__(user_id, name, pin, balance)


class SavingsAccount(Account):
    def __init__(self, user_id, name, pin, balance=0, interest_rate=0.05):
        super().__init__(user_id, name, pin, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        return {"message": f"Dodano odsetki: {interest}. Nowe saldo: {self.balance}"}

    def to_dict(self):
        data = super().to_dict()
        data["interest_rate"] = self.interest_rate
        return data
