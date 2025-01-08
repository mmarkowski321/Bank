import uuid
import smtplib
from app.config import Config
from email.mime.text import MIMEText
from app.db_utils import get_db
import psycopg2
import logging
import os
class Database:

    def register_user(self, user_data, account_data):
        try:
            db = get_db()
            cursor = db.cursor()

            user_id_uuid = str(uuid.uuid4())

            cursor.execute(
                'INSERT INTO users (user_id_uuid, first_name, middle_name, last_name, email, phone_number, date_of_birth) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (user_id_uuid, user_data['first_name'], user_data.get('middle_name', None),
                 user_data['last_name'], user_data['email'], user_data['phone_number'], user_data['date_of_birth'])
            )

            cursor.execute(
                'INSERT INTO accounts (pin, password, account_type, user_id_uuid) VALUES (%s, %s, %s, %s)',
                (account_data['pin'], account_data['password'], account_data['account_type'], user_id_uuid)
            )

            db.commit()
            cursor.close()

            self.send_email_with_user_id(user_data['email'], user_id_uuid)

            return {"message": "Account created. Please check your email for your unique user ID."}

        except psycopg2.IntegrityError as e:
            db.rollback()
            logging.error("Database integrity error: %s", e)
            return {"error": "A user with this email already exists"}
        except Exception as e:
            db.rollback()
            logging.error("Database error: %s", e)
            return {"error": "An error occurred during account creation"}

    def send_email_with_user_id(self, email, user_id_uuid):
        try:
            sender_email = Config.APP['sender']
            sender_password = Config.APP['password']
            smtp_server = "smtp.gmail.com"
            smtp_port = 587

            subject = "Welcome to Markbank - Your User ID"
            body = f"Hello,\n\nThank you for registering at Markbank. Your unique User ID is: {user_id_uuid}\n\nPlease keep it safe."
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = email

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)

            logging.info("Email sent successfully to %s", email)
        except Exception as e:
            logging.error("Failed to send email: %s", e)

    def login_user(self, user_id_uuid, password):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'SELECT account_id, user_id_uuid, password, balance FROM accounts WHERE user_id_uuid = %s AND password = %s',
            (user_id_uuid, password)
        )
        account = cursor.fetchone()
        cursor.close()
        return account

    def get_balance(self, user_id_uuid):
        cursor = get_db().cursor()
        cursor.execute(
            'SELECT balance FROM accounts WHERE user_id_uuid = %s',
            (user_id_uuid,)
        )
        balance = cursor.fetchone()
        cursor.close()
        return balance[0] if balance else None

    def deposit(self, user_id_uuid, amount):
        cursor = get_db().cursor()
        cursor.execute(
            'UPDATE accounts SET balance = balance + %s WHERE user_id_uuid = %s',
            (amount, user_id_uuid)
        )
        cursor.execute(
            'INSERT INTO transactions (user_id_uuid, type, amount, date) VALUES (%s, %s, %s, NOW())',
            (user_id_uuid, "Deposit", amount)
        )
        get_db().commit()
        cursor.close()
        return {"message": "Deposit successful"}

    def withdraw(self, user_id_uuid, amount):
        cursor = get_db().cursor()
        cursor.execute(
            'SELECT balance FROM accounts WHERE user_id_uuid = %s',
            (user_id_uuid,)
        )
        balance = cursor.fetchone()[0]

        if balance >= amount:
            cursor.execute(
                'UPDATE accounts SET balance = balance - %s WHERE user_id_uuid = %s',
                (amount, user_id_uuid)
            )
            cursor.execute(
                'INSERT INTO transactions (user_id_uuid, type, amount, date) VALUES (%s, %s, %s, NOW())',
                (user_id_uuid, "Withdrawal", amount)
            )
            get_db().commit()
            cursor.close()
            return {"message": "Withdrawal successful"}
        else:
            cursor.close()
            return {"error": "Insufficient funds"}

    def transfer(self, user_id_from_uuid, user_id_to_uuid, amount):
        cursor = get_db().cursor()

        cursor.execute(
            'SELECT balance FROM accounts WHERE user_id_uuid = %s',
            (user_id_to_uuid,)
        )
        if cursor.fetchone() is None:
            cursor.close()
            return {"error": "Recipient account does not exist"}

        cursor.execute(
            'SELECT balance FROM accounts WHERE user_id_uuid = %s',
            (user_id_from_uuid,)
        )
        balance_from = cursor.fetchone()[0]

        if balance_from >= amount:
            cursor.execute(
                'UPDATE accounts SET balance = balance - %s WHERE user_id_uuid = %s',
                (amount, user_id_from_uuid)
            )
            cursor.execute(
                'UPDATE accounts SET balance = balance + %s WHERE user_id_uuid = %s',
                (amount, user_id_to_uuid)
            )
            cursor.execute(
                'INSERT INTO transactions (user_id_uuid, type, amount, date) VALUES (%s, %s, %s, NOW())',
                (user_id_from_uuid, "Transfer Out", amount)
            )
            cursor.execute(
                'INSERT INTO transactions (user_id_uuid, type, amount, date) VALUES (%s, %s, %s, NOW())',
                (user_id_to_uuid, "Transfer In", amount)
            )
            get_db().commit()
            cursor.close()
            return {"message": "Transfer successful"}
        else:
            cursor.close()
            return {"error": "Insufficient funds in sender's account"}

    def get_transaction_history(self, user_id_uuid):
        try:
            cursor = get_db().cursor()
            query = '''
                SELECT type, amount, date 
                FROM transactions 
                WHERE user_id_uuid = %s 
                ORDER BY date DESC
            '''
            cursor.execute(query, (user_id_uuid,))
            transactions = cursor.fetchall()
            cursor.close()

            logging.debug(f"Raw transactions from DB: {transactions}")

            return [
                {"type": row[0], "amount": float(row[1]), "date": row[2].strftime('%Y-%m-%d %H:%M:%S')}
                for row in transactions
            ]
        except Exception as e:
            logging.error(f"Error fetching transaction history: {str(e)}")
            return []

    def update_user_details(self, user_id_uuid, email=None, phone_number=None):
        cursor = get_db().cursor()

        if email and phone_number:
            cursor.execute(
                'UPDATE users SET email = %s, phone_number = %s WHERE user_id_uuid = %s',
                (email, phone_number, user_id_uuid)
            )
        elif email:
            cursor.execute(
                'UPDATE users SET email = %s WHERE user_id_uuid = %s',
                (email, user_id_uuid)
            )
        elif phone_number:
            cursor.execute(
                'UPDATE users SET phone_number = %s WHERE user_id_uuid = %s',
                (phone_number, user_id_uuid)
            )

        get_db().commit()
        cursor.close()
        return {"message": "Personal details updated"}

    def update_password(self, user_id_uuid, new_password):
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'UPDATE accounts SET password = %s WHERE user_id_uuid = %s',
                (new_password, user_id_uuid)
            )
            db.commit()
            cursor.close()
            logging.info("Password updated successfully for user_id_uuid: %s", user_id_uuid)
            return {"message": "Password updated successfully"}
        except Exception as e:
            db.rollback()
            logging.error("Failed to update password for user_id_uuid %s: %s", user_id_uuid, e)
            return {"error": f"An error occurred: {str(e)}"}

    def getCurrentPassword(self, user_id_uuid):
        cursor = get_db().cursor()
        cursor.execute(
            'SELECT password FROM accounts WHERE user_id_uuid = %s', (user_id_uuid,)
        )
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]
        return None
