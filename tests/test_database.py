import pytest
from database import create_connection, register_user, get_balance, deposit, withdraw, transfer


@pytest.fixture
def setup_database():
    conn = create_connection(':memory:')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            pin TEXT NOT NULL,
            balance REAL DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            type TEXT,
            amount REAL,
            date TEXT,
            FOREIGN KEY (user_id) REFERENCES accounts (user_id)
        )
    ''')

    conn.commit()
    yield conn
    conn.close()


def test_register_user(setup_database):
    conn = setup_database
    register_user('123', 'John Doe', '1234', conn)
    balance = get_balance('123', conn)
    assert balance == 0


def test_deposit(setup_database):
    conn = setup_database
    register_user('123', 'John Doe', '1234', conn)
    deposit('123', 100, conn)
    balance = get_balance('123', conn)
    assert balance == 100


def test_withdraw(setup_database):
    conn = setup_database
    register_user('123', 'John Doe', '1234', conn)
    deposit('123', 100, conn)
    withdraw('123', 50, conn)
    balance = get_balance('123', conn)
    assert balance == 50


def test_withdraw_insufficient_funds(setup_database):
    conn = setup_database
    register_user('123', 'John Doe', '1234', conn)
    deposit('123', 50, conn)
    result = withdraw('123', 100, conn)
    balance = get_balance('123', conn)
    assert balance == 50
    assert result is False


def test_transfer(setup_database):
    conn = setup_database
    register_user('123', 'John Doe', '1234', conn)
    register_user('456', 'Jane Doe', '5678', conn)
    deposit('123', 200, conn)
    transfer('123', '456', 100, conn)
    balance_from = get_balance('123', conn)
    balance_to = get_balance('456', conn)
    assert balance_from == 100
    assert balance_to == 100
