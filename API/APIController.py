from flask import Flask, request, jsonify
from flask_cors import CORS
from API import connection
import transactions

# defining the flask app and setting up cors for the url
app = Flask(__name__)
cors = CORS(app, resources={
    r"/*": {"origin": "*"}
})

# Setting up connection with algorand client
algod_client = connection.algo_conn()
myindexer = connection.connect_indexer()


# Payment transaction of USDC
@app.route('/blockchain/usdc_payment', methods=["POST"])
def txn():
    # get the details
    user_details = request.get_json()
    sender = user_details['sender']
    receiver = user_details['receiver']
    amt = int(user_details['amount'])*10**6
    note = user_details['note']

    # check the balance of the asset and the wallet
    if transactions.check_balance_with_asset(algod_client, sender, 1000, amt) == "True":

        try:
            # send the data to blockchain
            txn_object = transactions.payment_txn(algod_client, sender, receiver, amt, note)
            return jsonify(txn_object), 200
        except Exception as error:
            return jsonify({'message': str(error)}), 500

    elif transactions.check_balance_with_asset(algod_client, sender, 0.001, amt) == "False":
        return jsonify({'message': f"Wallet balance low!"}), 500

    # return as a message if any error occurs
    else:
        return jsonify(transactions.check_balance_with_asset(algod_client, sender, 1000, amt)), 400


# asset opt-in transaction
@app.route('/blockchain/usdc_optin', methods=["POST"])
def optin_txn():
    # get the details
    txn_details = request.get_json()
    sender = txn_details['sender']

    # check the balance of the sender
    if transactions.check_balance(algod_client, sender, 1000) == "True":

        try:
            txn_object = transactions.optin_txn(algod_client, sender)
            return jsonify(txn_object), 200
        except Exception as error:
            return jsonify({'message': str(error)}), 500

    elif transactions.check_balance(algod_client, sender, 1000) == "False":
        return jsonify({"message": "Wallet balance low!"}), 500

    # return as a message if any error occurs
    else:
        return jsonify(transactions.check_balance(algod_client, sender, 1000)), 400


# sign transaction
@app.route('/blockchain/sign_transaction', methods=['POST'])
def sign_txn():
    # get the details
    txn_details = request.get_json()
    sender = txn_details['sender']
    private_key = txn_details['private_key']
    receiver = txn_details['receiver']
    amt = txn_details['amount']
    note = txn_details['transaction_note']

    if transactions.check_balance(algod_client, sender, 1000) == 'True':
        try:
            singed_txn = transactions.sign_payment_txn(algod_client, sender, private_key, receiver, amt, note)
            return jsonify(singed_txn), 200
        except Exception as error:
            return jsonify({'message': str(error)}), 500

    elif transactions.check_balance(algod_client, sender, 1000) == "False":
        return jsonify({"message": "Wallet balance low!"}), 500

    # return as a message if any error occurs
    else:
        return jsonify(transactions.check_balance(algod_client, sender, 1000)), 400


# running the API
if __name__ == "__main__":
    app.run(debug=True, port=5000)
