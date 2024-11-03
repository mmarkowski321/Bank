from flask import current_app, g
import psycopg2
import psycopg2.extras

def get_db():
    if 'db' not in g:
        try:
            config = current_app.config['DATABASE']
            g.db = psycopg2.connect(**config)
            print("Połączenie z bazą danych zostało nawiązane.")
        except psycopg2.OperationalError as e:
            print("Błąd połączenia z bazą danych:", e)
            g.db = None
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
        print("Połączenie z bazą danych zostało zamknięte.")
