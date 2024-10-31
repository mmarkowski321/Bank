from flask import current_app, g
import psycopg2

def get_db():
    if 'db' not in g:
        config = current_app.config['DATABASE']
        g.db = psycopg2.connect(**config)
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
    