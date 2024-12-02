import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE = {
        'dbname': os.getenv('DATABASE_NAME'),
        'user': os.getenv('DATABASE_USER'),
        'password': os.getenv('DATABASE_PASSWORD'),
        'host': os.getenv('DATABASE_HOST'),
        'port': os.getenv('DATABASE_PORT')
    }

    APP = {
        'sender': os.getenv('APP_SENDER'),
        'password': os.getenv('APP_PASSWORD')
    }
