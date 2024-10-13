import pytest
from database import Database

def test_database_connection():
    db = Database(":memory:")
    assert db is not None

def test_create_account_in_db():
    db = Database(":memory:")
    db.create_account("John Doe", 100)
    result = db.get_account("John Doe")
    assert result is not None
    assert result['balance'] == 100

def test_deposit_to_account():
    db = Database(":memory:")
    db.create_account("John Doe", 100)
    db.deposit("John Doe", 50)
    result = db.get_account("John Doe")
    assert result['balance'] == 150
