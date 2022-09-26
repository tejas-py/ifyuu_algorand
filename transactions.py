from algosdk.future import transaction
from algosdk import encoding

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


# check the balance of the account
def check_balance(client, wallet_address, amt):
    try:
        account_i = client.account_info(wallet_address)
        min_balance = account_i['min-balance']
        balance = account_i['amount']

        if balance >= amt and balance > min_balance:
            return "True"
        else:
            return "False"
    except Exception as error:
        return {'message': error}


# check the wallet address and the amount
def check_balance_with_asset(client, wallet_address, amt, payment_amt, asset_id=asset):
    global asset_amt
    try:
        # check the balance in the account
        account_info = client.account_info(wallet_address)
        min_balance = account_info['min-balance']
        balance = account_info['amount']

        try:
            # search if asset amount and if asset exist or not
            assets_list = account_info['assets']
            for one_asset in assets_list:
                if asset_id == one_asset['asset-id']:
                    asset_amt = one_asset['amount']
                    break
                else:
                    asset_amt = 0
        # If the asset doesn't exist return the message
        except Exception as asset_error:
            return {'message':  f'Error: {asset_error}! USDC does not exist in the account.'}

        # check if the balance is satisfied
        if balance >= amt and asset_amt >= payment_amt and balance > min_balance:
            return "True"
        else:
            return "False"
    # return if any error occurs
    except Exception as error:
        return {'message': error}


# sign-transaction
def sign_payment_txn(client, sender, private_key, receiver, amt, note):

    # define the params
    params = client.suggested_params()

    # make the transaction object
    txn = transaction.AssetTransferTxn(sender, params, receiver, amt, index=asset, note=note)

    print("Signing Transaction...")
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    transaction.wait_for_confirmation(client, tx_id)
    print(f"Transaction Successful with Transaction Id: {tx_id}")

    # display results
    transaction_response = client.pending_transaction_info(tx_id)

    return transaction_response

