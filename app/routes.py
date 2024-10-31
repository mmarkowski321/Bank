from flask import request, jsonify
from app import app
from database import Database
from flask import render_template, request, jsonify
# Instancja klasy Database
db = Database()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user_id = data['user_id']
    name = data['name']
    pin = data['pin']

    result = db.register_user(user_id, name, pin)
    status_code = 201 if "message" in result else 400
    return jsonify(result), status_code


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = data['user_id']
    pin = data['pin']

    account = db.login_user(user_id, pin)
    if account:
        return jsonify({
            "user_id": account[0],
            "name": account[1],
            "balance": account[3]
        }), 200
    return jsonify({"error": "Nieprawidłowy identyfikator użytkownika lub PIN"}), 401


@app.route('/balance/<user_id>', methods=['GET'])
def balance(user_id):
    balance = db.get_balance(user_id)
    if balance is not None:
        return jsonify({"user_id": user_id, "balance": balance}), 200
    return jsonify({"error": "Konto nie istnieje"}), 404


@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.get_json()
    user_id = data['user_id']
    amount = data['amount']

    result = db.deposit(user_id, amount)
    return jsonify(result), 200 if "message" in result else 404


@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.get_json()
    user_id = data['user_id']
    amount = data['amount']

    result = db.withdraw(user_id, amount)
    return jsonify(result), 200 if "message" in result else 404


@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.get_json()
    user_id_from = data['user_id_from']
    user_id_to = data['user_id_to']
    amount = data['amount']

    result = db.transfer(user_id_from, user_id_to, amount)
    return jsonify(result), 200 if "message" in result else 404


@app.route('/transaction_history/<user_id>', methods=['GET'])
def transaction_history(user_id):
    transactions = db.get_transaction_history(user_id)
    if transactions:
        return jsonify(transactions), 200
    return jsonify({"error": "Brak transakcji lub konto nie istnieje"}), 404
