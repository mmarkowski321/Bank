from flask import render_template, request, jsonify, redirect, url_for
from database import Database
import logging
db = Database()
logging.basicConfig(level=logging.DEBUG)
def initialize_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/dashboard')
    def dashboard():
        user_id = request.args.get('user_id')
        if not user_id:
            return redirect(url_for('index'))
        return render_template('dashboard.html', user_id=user_id)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'GET':
            return render_template('register.html')
        elif request.method == 'POST':
            data = request.get_json()
            logging.debug("Received data for registration: %s", data)  # Logowanie danych

            user_data = {
                'first_name': data.get('first_name'),
                'middle_name': data.get('middle_name'),
                'last_name': data.get('last_name'),
                'email': data.get('email'),
                'phone_number': data.get('phone'),
                'date_of_birth': data.get('date_of_birth')
            }

            account_data = {
                'pin': data.get('pin'),
                'password': data.get('password'),
                'account_type': data.get('account_type')
            }

            result = db.register_user(user_data, account_data)
            status_code = 201 if "message" in result else 400
            return jsonify(result), status_code

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        logging.debug("Received login data: %s", data)  # Log incoming data for debugging

        user_id = data.get('user_id')
        password = data.get('password')

        account = db.login_user(user_id, password)
        if account:
            logging.debug("Login successful for user_id: %s", user_id)
            return jsonify({
                "account_id": account[0],
                "user_id": account[1],
                "balance": account[3]
            }), 200
        else:
            logging.debug("Login failed for user_id: %s", user_id)
            return jsonify({"error": "Invalid user ID or Password"}), 401

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

    @app.route('/transactions/<user_id>', methods=['GET'])
    def transaction_history(user_id):
        transactions = db.get_transaction_history(user_id)
        if transactions:
            return jsonify(transactions), 200
        return jsonify({"error": "No transactions found"}), 404

    @app.route('/update_user_details', methods=['POST'])
    def update_user_details():
        data = request.get_json()
        user_id = data['user_id']
        email = data['email']
        phone_number = data['phone']

        result = db.update_user_details(user_id, email, phone_number)
        return jsonify(result), 200

    @app.route('/profile.html')
    def profile_page():
        return render_template('profile.html')

    @app.route('/update_password', methods=['POST'])
    def update_password():
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            current_password = data.get('current_password')
            new_password = data.get('new_password')

            if not user_id or not current_password or not new_password:
                return jsonify({"error": "Missing required fields"}), 400

            # Retrieve the current password from the database
            stored_password = db.getCurrentPassword(user_id)
            if not stored_password:
                return jsonify({"error": "User not found"}), 404

            # Check if the current password matches
            if current_password != stored_password:
                return jsonify({"error": "Current password is incorrect"}), 401

            # Update the password in the database
            result = db.update_password(user_id, new_password)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500



    @app.route('/get_current_password', methods=['POST'])
    def get_current_password():
        try:
            data = request.get_json()
            user_id = data.get('user_id')

            if not user_id:
                return jsonify({"error": "Missing user ID"}), 400

            current_password = db.getCurrentPassword(user_id)
            if current_password is None:
                return jsonify({"error": "User not found"}), 404

            return jsonify({"current_password": current_password}), 200
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500


