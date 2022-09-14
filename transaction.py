from algosdk.future import transaction
from algosdk import encoding


# payment transaction
def payment_txn(client, sender, receiver, amt, note):

    # define the params
    params = client.suggested_params()

    # do the payment
    txn = transaction.PaymentTxn(sender, params, receiver, amt, note=note)

    txngrp = [{'txn': encoding.msgpack_encode(txn)}]

    return txngrp
