from flask import Flask, request, jsonify
from flask_cors import CORS
import transactions, common_functions
from API import connection

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
    amt = int(user_details['amount']*10**6)
    note = user_details['note']

    # check the balance of the asset and the wallet
    sender_wallet_information = common_functions.check_balance_with_asset(algod_client, sender, 1000, amt)
    if sender_wallet_information == "True":

        # Check receiver wallet and if he has optin to the asset
        receiver_wallet_information = common_functions.check_receiver_wallet(algod_client, receiver)
        if receiver_wallet_information == "True":
            try:
                # send the data to blockchain
                txn_object = transactions.payment_txn(algod_client, sender, receiver, amt, note)
                return jsonify(txn_object), 200
            except Exception as error:
                return jsonify({'message': str(error)}), 500
        else:
            return jsonify(receiver_wallet_information), 400

    elif sender_wallet_information == "False":
        return jsonify({'message': f"Wallet balance low!"}), 500

    # return as a message if any error occurs
    else:
        return jsonify(sender_wallet_information), 400


# asset opt-in transaction
@app.route('/blockchain/usdc_optin', methods=["POST"])
def optin_txn():
    # get the details
    txn_details = request.get_json()
    sender = txn_details['sender']

    # check the balance of the sender
    sender_wallet_information = common_functions.check_balance(algod_client, sender, 1000)
    if sender_wallet_information == "True":

        try:
            txn_object = transactions.optin_txn(algod_client, sender)
            return jsonify(txn_object), 200
        except Exception as error:
            return jsonify({'message': str(error)}), 500

    elif sender_wallet_information == "False":
        return jsonify({"message": "Wallet balance low!"}), 500

    # return as a message if any error occurs
    else:
        return jsonify(sender_wallet_information), 400


# sign transaction
@app.route('/blockchain/sign_transaction', methods=['POST'])
def sign_txn():
    # get the details
    txn_details = request.get_json()
    sender = txn_details['sender']
    mnemonics = txn_details['mnemonics']
    receiver = txn_details['receiver']
    amt = int(txn_details['amount']*10**6)
    note = txn_details['transaction_note']

    # check the balance of the asset and the wallet
    sender_wallet_information = common_functions.check_balance_with_asset(algod_client, sender, 1000, amt)
    if sender_wallet_information == 'True':

        # Check receiver wallet and if he has optin to the asset
        receiver_wallet_information = common_functions.check_receiver_wallet(algod_client, receiver)
        if receiver_wallet_information == "True":
            try:
                # send the data to blockchain
                singed_txn = transactions.sign_payment_txn(algod_client, sender, mnemonics, receiver, amt, note)
                return jsonify(singed_txn), 200
            except Exception as error:
                return jsonify({'message': str(error)}), 500
        else:
            return jsonify(receiver_wallet_information), 400

    elif sender_wallet_information == "False":
        return jsonify({"message": "Wallet balance low!"}), 500

    # return as a message if any error occurs
    else:
        return jsonify(sender_wallet_information), 400


# running the API
if __name__ == "__main__":
    app.run(debug=True, port=5000)
