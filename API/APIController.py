from flask import Flask, request, jsonify
from flask_cors import CORS
from API import connection
import transactions

# defining the flask app and setting up cors
app = Flask(__name__)
cors = CORS(app, resources={
    r"/*": {"origin": "*"}
})

# Setting up connection with algorand client
algod_client = connection.algo_conn()
myindexer = connection.connect_indexer()


# Payment transaction
@app.route('/blockchain/usdc_payment', methods=["POST"])
def txn():
    # get the details
    user_details = request.get_json()
    sender = user_details['sender']
    receiver = user_details['receiver']
    amt = int(user_details['amount'])*10**6
    note = user_details['note']

    if transactions.check_balance(myindexer, sender, 1000, amt) == "True":

        try:
            # send the data to blockchain
            txn_object = transactions.payment_txn(algod_client, sender, receiver, amt, note)
            return jsonify(txn_object), 200
        except Exception as error:
            return jsonify({'message': error}), 500

    elif transactions.check_balance(myindexer, sender, 0.001, amt) == "False":
        return jsonify({'message': f"Wallet Balance low"}), 400

    else:
        return jsonify(transactions.check_balance(myindexer, sender, 1000, amt)), 400


# running the API
if __name__ == "__main__":
    app.run(debug=True, port=4000)
