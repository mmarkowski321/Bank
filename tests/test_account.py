import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from account import Account, SavingsAccount, CheckingAccount

def test_create_account():
    account = Account("123", "John Doe", "1234", 100)
    assert account.get_user_id() == "123"
    assert account.get_balance() == 100

def test_deposit():
    account = Account("123", "John Doe", "1234", 100)
    account.deposit(50)
    assert account.get_balance() == 150

def test_withdraw():
    account = Account("123", "John Doe", "1234", 100)
    result = account.withdraw(50)
    assert result is True
    assert account.get_balance() == 50

def test_withdraw_insufficient_funds():
    account = Account("123", "John Doe", "1234", 100)
    result = account.withdraw(150)
    assert result is False
    assert account.get_balance() == 100

def test_savings_account_interest():
    savings_account = SavingsAccount("123", "John Doe", "1234", 1000, interest_rate=0.05)
    interest = savings_account.add_interest()
    assert interest == 50
    assert savings_account.get_balance() == 1050

def test_checking_account_withdraw_with_fee():
    checking_account = CheckingAccount("123", "John Doe", "1234", 100, transaction_fee=2.0)
    result = checking_account.withdraw(50)
    assert result is True
    assert checking_account.get_balance() == 48  # 50 + 2 (transaction fee) = 52, więc pozostałe saldo to 48
