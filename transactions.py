from algosdk.future.transaction import *
from algosdk import encoding, mnemonic
from API.connection import connect_indexer

# declare the asset
asset = 10458941

# indexer client
indexer_client = connect_indexer()


# get the current rount
def blockchain_round():
    res = indexer_client.health()
    latest_round = res['round']
    # print()
    return latest_round


# USDC asset transfer transaction
def payment_txn(client, sender, receiver, amt, note):

    # define the params
    params = client.suggested_params()

    # make the transaction object
    txn = AssetTransferTxn(sender, params, receiver, int(amt), asset, note=note)
    print(txn)
    # encode the transaction object
    txngrp = [{'txn': encoding.msgpack_encode(txn)}]

    return txngrp


# Asset opt-in transaction
def optin_txn(client, sender):

    # define the params
    params = client.suggested_params()

    # make the transaction object
    txn = AssetTransferTxn(sender, params, sender, 0, asset)
    # encode the transaction object
    txngrp = [{'txn': encoding.msgpack_encode(txn)}]

    return txngrp


# sign-transaction
def sign_payment_txn(client, sender, mnemonic_keys, receiver, amt, note):
    # derive private key
    private_key = mnemonic.to_private_key(mnemonic_keys)

    # define the params
    params = client.suggested_params()
    params.fee = 1000
    params.flat_fee = True

    # make the transaction object
    txn = AssetTransferTxn(sender, params, receiver, amt, asset, note=note)

    print("Signing Transaction...")
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(client, tx_id)
    print(f"Transaction Successful with Transaction Id: {tx_id}")
    return {'message': tx_id}


blockchain_round()
