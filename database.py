from app.db_utils import get_db
import psycopg2

class Database:
    def register_user(self, user_id, name, pin):
        """Rejestracja nowego użytkownika."""
        try:
            cursor = get_db().cursor()
            cursor.execute(
                'INSERT INTO accounts (user_id, name, pin) VALUES (%s, %s, %s)',
                (user_id, name, pin)
            )
            get_db().commit()
            cursor.close()
            return {"message": "Konto zostało utworzone"}
        except psycopg2.IntegrityError:
            get_db().rollback()
            return {"error": "Użytkownik o tym ID już istnieje"}

    def login_user(self, user_id, pin):
        """Logowanie użytkownika na podstawie ID i PIN-u."""
        cursor = get_db().cursor()
        cursor.execute(
            'SELECT * FROM accounts WHERE user_id = %s AND pin = %s',
            (user_id, pin)
        )
        account = cursor.fetchone()
        cursor.close()
        return account

    def get_balance(self, user_id):
        """Pobiera saldo użytkownika."""
        cursor = get_db().cursor()
        cursor.execute(
            'SELECT balance FROM accounts WHERE user_id = %s',
            (user_id,)
        )
        balance = cursor.fetchone()
        cursor.close()
        return balance[0] if balance else None

    def deposit(self, user_id, amount):
        """Wpłata środków na konto użytkownika."""
        cursor = get_db().cursor()
        cursor.execute(
            'UPDATE accounts SET balance = balance + %s WHERE user_id = %s',
            (amount, user_id)
        )
        cursor.execute(
            'INSERT INTO transactions (user_id, type, amount, date) VALUES (%s, %s, %s, NOW())',
            (user_id, "Deposit", amount)
        )
        get_db().commit()
        cursor.close()
        return {"message": "Wpłata została zrealizowana"}

    def withdraw(self, user_id, amount):
        """Wypłata środków z konta użytkownika."""
        cursor = get_db().cursor()
        cursor.execute(
            'SELECT balance FROM accounts WHERE user_id = %s',
            (user_id,)
        )
        balance = cursor.fetchone()[0]

        if balance >= amount:
            cursor.execute(
                'UPDATE accounts SET balance = balance - %s WHERE user_id = %s',
                (amount, user_id)
            )
            cursor.execute(
                'INSERT INTO transactions (user_id, type, amount, date) VALUES (%s, %s, %s, NOW())',
                (user_id, "Withdrawal", amount)
            )
            get_db().commit()
            cursor.close()
            return {"message": "Wypłata została zrealizowana"}
        else:
            cursor.close()
            return {"error": "Brak wystarczających środków"}

    def transfer(self, user_id_from, user_id_to, amount):
        """Przelew między użytkownikami."""
        cursor = get_db().cursor()

        # Sprawdzenie istnienia konta docelowego
        cursor.execute(
            'SELECT balance FROM accounts WHERE user_id = %s',
            (user_id_to,)
        )
        if cursor.fetchone() is None:
            cursor.close()
            return {"error": "Konto docelowe nie istnieje"}

        # Sprawdzenie wystarczających środków
        cursor.execute(
            'SELECT balance FROM accounts WHERE user_id = %s',
            (user_id_from,)
        )
        balance_from = cursor.fetchone()[0]

        if balance_from >= amount:
            cursor.execute(
                'UPDATE accounts SET balance = balance - %s WHERE user_id = %s',
                (amount, user_id_from)
            )
            cursor.execute(
                'UPDATE accounts SET balance = balance + %s WHERE user_id = %s',
                (amount, user_id_to)
            )
            cursor.execute(
                'INSERT INTO transactions (user_id, type, amount, date) VALUES (%s, %s, %s, NOW())',
                (user_id_from, "Transfer Out", amount)
            )
            cursor.execute(
                'INSERT INTO transactions (user_id, type, amount, date) VALUES (%s, %s, %s, NOW())',
                (user_id_to, "Transfer In", amount)
            )
            get_db().commit()
            cursor.close()
            return {"message": "Transfer został zrealizowany"}
        else:
            cursor.close()
            return {"error": "Brak wystarczających środków na koncie nadawcy"}

    def get_transaction_history(self, user_id):
        """Pobiera historię transakcji użytkownika."""
        cursor = get_db().cursor()
        cursor.execute(
            'SELECT type, amount, date FROM transactions WHERE user_id = %s ORDER BY date DESC',
            (user_id,)
        )
        transactions = cursor.fetchall()
        cursor.close()
        return [{"type": t[0], "amount": t[1], "date": t[2]} for t in transactions]
