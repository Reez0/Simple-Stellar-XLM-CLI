from stellar_sdk.keypair import Keypair
import json
import requests
from .models import Account


def create_account(db, account_type):
    pair = Keypair.random()
    try:
        account = Account.create(public=pair.public_key, secret=pair.secret, type=account_type )
        account.save()
    except Exception as e:
        print(e)
        return False
    return True

def fund_account(account_data):
    response = requests.get(f"https://friendbot.stellar.org?addr={account_data.public}")
    if response.status_code == 200:
        return True
    else:
        print(response.text)
        return False

def get_balances():
    pass