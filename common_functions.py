# declare the asset
asset = 10458941


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
        try:
            # check the balance in the account
            account_info = client.account_info(wallet_address)
            min_balance = account_info['min-balance']
            balance = account_info['amount']
        except Exception as wallet_error:
            return {'message': f"Wallet doesn't Exist! {wallet_error}"}

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


# Check the receiver has the USDC
def check_receiver_wallet(client, wallet_address, asset_id=asset):
    global asset_amt
    try:
        try:
            # check the balance in the account
            account_info = client.account_info(wallet_address)
        except Exception as wallet_error:
            return {'message': f"Receiver Wallet doesn't Exist! {wallet_error}"}

        try:
            # search if asset amount and if asset exist or not
            assets_list = account_info['assets']
            for one_asset in assets_list:
                if asset_id == one_asset['asset-id']:
                    asset_amt = one_asset['amount']
                    return "True"
                else:
                    return {'message': f'Receiver has not Opt-in to the Asset: {asset}.'}
        # If the asset doesn't exist return the message
        except Exception as asset_error:
            return {'message':  f'Error: {asset_error}! USDC does not exist in the account.'}

    # return if any error occurs
    except Exception as error:
        return {'message': error}

