from account import Account
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_create_account():
    account = Account("John Doe", 100)
    assert account.owner == "John Doe"
    assert account.balance == 100

def test_deposit():
    account = Account("John Doe", 100)
    result = account.deposit(50)
    assert result == True
    assert account.balance == 150

def test_negative_deposit():
    account = Account("Jane Doe", 100)
    result = account.deposit(-50)
    assert result == False
    assert account.balance == 100

def test_withdraw():
    account = Account("John Doe", 100)
    result = account.withdraw(50)
    assert result == True
    assert account.balance == 50

def test_overdraw():
    account = Account("Jane Doe", 100)
    result = account.withdraw(150)
    assert result == False
    assert account.balance == 100
