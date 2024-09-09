import sqlite3


def create_connection():
    """Tworzy połączenie z bazą danych SQLite."""
    conn = sqlite3.connect('bank.db')
    return conn


def create_table():
    conn = create_connection()
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
    conn.close()


def register_user(user_id, name, pin):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO accounts (user_id, name, pin) VALUES (?, ?, ?)', (user_id, name, pin))
        conn.commit()
        print(f"Konto dla użytkownika {name} zostało utworzone.")
    except sqlite3.IntegrityError:
        print("Użytkownik o tym ID już istnieje.")
    conn.close()


def login_user(user_id, pin):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accounts WHERE user_id = ? AND pin = ?', (user_id, pin))
    account = cursor.fetchone()
    conn.close()
    return account


def delete_user(user_id, name, pin):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM accounts WHERE user_id = ? AND pin = ?', (user_id, pin))
        conn.commit()
        print(f"Konto dla użytkownika {name} zostało usunięte")
    except sqlite3.IntegrityError:
        print("Użytkownik o tych danych nie istnieje.")


def get_balance(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT balance FROM accounts WHERE user_id = ?', (user_id,))
    balance = cursor.fetchone()
    conn.close()
    return balance[0] if balance else None


def deposit(user_id, amount):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE accounts SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
    cursor.execute('INSERT INTO transactions (user_id, type, amount, date) VALUES (?, "Deposit", ?, datetime("now"))',
                   (user_id, amount))
    conn.commit()
    conn.close()


def withdraw(user_id, amount):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT balance FROM accounts WHERE user_id = ?', (user_id,))
    balance = cursor.fetchone()[0]

    if balance >= amount:
        cursor.execute('UPDATE accounts SET balance = balance - ? WHERE user_id = ?', (amount, user_id))
        cursor.execute(
            'INSERT INTO transactions (user_id, type, amount, date) VALUES (?, "Withdrawal", ?, datetime("now"))',
            (user_id, amount))
        conn.commit()
        print("Wypłata zrealizowana.")
    else:
        print("Brak wystarczających środków.")
    conn.close()


def transfer(user_id_from, user_id_to, amount):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT balance FROM accounts WHERE user_id = ?', (user_id_to,))
    if cursor.fetchone() is None:
        print("Konto docelowe nie istnieje.")
        conn.close()
        return False

    cursor.execute('SELECT balance FROM accounts WHERE user_id = ?', (user_id_from,))
    balance_from = cursor.fetchone()[0]

    if balance_from >= amount:
        cursor.execute('UPDATE accounts SET balance = balance - ? WHERE user_id = ?', (amount, user_id_from))
        cursor.execute('UPDATE accounts SET balance = balance + ? WHERE user_id = ?', (amount, user_id_to))
        cursor.execute(
            'INSERT INTO transactions (user_id, type, amount, date) VALUES (?, "Transfer Out", ?, datetime("now"))',
            (user_id_from, -amount))
        cursor.execute(
            'INSERT INTO transactions (user_id, type, amount, date) VALUES (?, "Transfer In", ?, datetime("now"))',
            (user_id_to, amount))

        conn.commit()
        print("Transfer zrealizowany.")
        conn.close()
        return True
    else:
        print("Brak wystarczających środków na koncie nadawcy.")
        conn.close()
        return False


def get_transaction_history(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT type, amount, date FROM transactions WHERE user_id = ? ORDER BY date DESC', (user_id,))
    transactions = cursor.fetchall()
    conn.close()
    return transactions
