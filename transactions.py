from algosdk.future import transaction
from algosdk import encoding, mnemonic

# declare the asset
asset = 10458941


# USDC asset transfer transaction
def payment_txn(client, sender, receiver, amt, note):

    # define the params
    params = client.suggested_params()

    # make the transaction object
    txn = transaction.AssetTransferTxn(sender, params, receiver, amt, index=asset, note=note)

    # encode the transaction object
    txngrp = [{'txn': encoding.msgpack_encode(txn)}]

    return txngrp


# Asset opt-in transaction
def optin_txn(client, sender):

    # define the params
    params = client.suggested_params()

    # make the transaction object
    txn = transaction.AssetTransferTxn(sender, params, sender, 0, asset)
    # encode the transaction object
    txngrp = [{'txn': encoding.msgpack_encode(txn)}]

    return txngrp


# sign-transaction
def sign_payment_txn(client, sender, mnemonic_keys, receiver, amt, note):

    # derive private key
    private_key = mnemonic.to_private_key(mnemonic_keys)

    # define the params
    params = client.suggested_params()

    # make the transaction object
    txn = transaction.AssetTransferTxn(sender, params, receiver, amt*1_000_000, index=asset, note=note)

    print("Signing Transaction...")
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    transaction.wait_for_confirmation(client, tx_id)
    print(f"Transaction Successful with Transaction Id: {tx_id}")

    return {'message': tx_id}
