from flask import Flask, request, jsonify
from flask_cors import CORS
from API import connection
import transaction

# defining the flask app and setting up cors
app = Flask(__name__)
cors = CORS(app, resources={
    r"/*": {"origin": "*"}
})

# Setting up connection with algorand client
algod_client = connection.algo_conn()
myindexer = connection.connect_indexer()


# check the wallet address and the amount
def check_balance(wallet_address, amt):
    try:
        account_info = myindexer.account_info(wallet_address)
        balance = account_info['account']['amount']
        if balance >= amt:
            return "True"
        else:
            return "False"
    except Exception as error:
        return {'message': error}


# Payment transaction
@app.route('/blockchain_payment', methods=["POST"])
def txn():
    # get the details
    user_details = request.get_json()
    sender = user_details['sender']
    receiver = user_details['receiver']
    amt = user_details['amount']
    note = user_details['note']

    if check_balance(sender, amt) == "True":

        try:
            # send the data to blockchain
            txn_object = transaction.payment_txn(algod_client, sender, receiver, amt, note)
            return jsonify(txn_object), 200
        except Exception as error:
            return jsonify({'message': error}), 500

    elif check_balance(sender, amt) == "False":
        return jsonify({'message': f"Wallet Balance below {amt}"}), 400

    else:
        return jsonify(check_balance(sender, amt)), 400


# running the API
if __name__ == "__main__":
    app.run(debug=True, port=4000)
