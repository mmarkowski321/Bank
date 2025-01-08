import os
import pytest
from flask import Flask
from app.routes import initialize_routes
from unittest.mock import MagicMock

@pytest.fixture
def client():
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', 'static'))

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config['TESTING'] = True

    from database import Database
    Database.get_balance = MagicMock(return_value=500)
    Database.register_user = MagicMock(return_value={"message": "User registered successfully"})
    Database.login_user = MagicMock(return_value=(1, "1234", "Milosz", 100))
    Database.deposit = MagicMock(return_value={"message": "Deposit successful"})
    Database.withdraw = MagicMock(return_value={"message": "Withdraw successful"})
    Database.transfer = MagicMock(return_value={"message": "Transfer successful"})
    Database.get_transaction_history = MagicMock(return_value=[
        {"type": "Deposit", "amount": 100.0, "date": "2024-06-15"},
        {"type": "Withdraw", "amount": 50.0, "date": "2024-06-14"}
    ])

    initialize_routes(app)

    return app.test_client()


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Sign in" in response.data


def test_dashboard_with_user_id(client):
    response = client.get('/dashboard?user_id=1234')
    assert response.status_code == 200
    assert b"Dashboard" in response.data

def test_dashboard_without_user_id(client):
    response = client.get('/dashboard')
    assert response.status_code == 302

def test_register_post(client):
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "123456789",
        "date_of_birth": "1990-01-01",
        "pin": "1234",
        "password": "password123",
        "account_type": "savings"
    }
    response = client.post('/register', json=data)
    assert response.status_code == 201
    assert response.json["message"] == "User registered successfully"

def test_login(client):
    data = {"user_id": "1234", "password": "password123"}
    response = client.post('/login', json=data)
    assert response.status_code == 200
    assert "balance" in response.json


def test_balance(client):
    response = client.get('/balance/1234')
    assert response.status_code == 200
    assert response.json["balance"] == 500


def test_deposit(client):
    data = {"user_id": "1234", "amount": 100}
    response = client.post('/deposit', json=data)
    assert response.status_code == 200
    assert response.json["message"] == "Deposit successful"


def test_withdraw(client):
    data = {"user_id": "1234", "amount": 50}
    response = client.post('/withdraw', json=data)
    assert response.status_code == 200
    assert response.json["message"] == "Withdraw successful"


def test_transfer(client):
    data = {"user_id_from": "1234", "user_id_to": "5678", "amount": 50}
    response = client.post('/transfer', json=data)
    assert response.status_code == 200
    assert response.json["message"] == "Transfer successful"


def test_transaction_history(client):
    response = client.get('/transactions/1234')
    assert response.status_code == 200
    assert b"Deposit" in response.data
    assert b"Withdraw" in response.data
