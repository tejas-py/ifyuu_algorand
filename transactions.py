from algosdk.future import transaction
from algosdk import encoding


# payment transaction
def payment_txn(client, sender, receiver, amt, note):

    # define the params
    params = client.suggested_params()

    # do the payment
    txn = transaction.AssetTransferTxn(sender, params, receiver, amt, index=10458941, note=note)

    txngrp = [{'txn': encoding.msgpack_encode(txn)}]

    return txngrp


# check the wallet address and the amount
def check_balance(indexer_client, wallet_address, amt, payment_amt, asset_id=10458941):
    global asset_amt
    try:
        # check the balance in the account
        account_info = indexer_client.account_info(wallet_address)
        balance = account_info['account']['amount']

        try:
            # search if asset amount and if asset exist or not
            assets_list = account_info['account']['assets']
            for one_asset in assets_list:
                if asset_id == one_asset['asset-id']:
                    asset_amt = one_asset['amount']
                    break
                else:
                    asset_amt = 0
        except Exception as asset_error:
            return {'message':  f'Error: {asset_error}! USDC does not exist in the account.'}

        # check if the balance is satisfied
        if balance >= amt and asset_amt >= payment_amt:
            return "True"
        else:
            return "False"
    except Exception as error:
        return {'message': error}
