from .models import Account
from stellar_sdk import account, memo
from stellar_sdk.sep.mnemonic import Language
from stellar_sdk.transaction_builder import TransactionBuilder
from stellar_sdk.exceptions import NotFoundError, BadResponseError, BadRequestError, SdkError
from stellar_sdk.asset import Asset
from stellar_sdk.keypair import Keypair
from stellar_sdk.network import Network
from stellar_sdk.server import Server

def new_payment(to,memo,amount,asset_name):
    server = Server(horizon_url="https://horizon-testnet.stellar.org")
    admin_account = Account.get(Account.type == 'issuer')
    issuing_keypair = Keypair.from_secret(admin_account.secret)
    issuing_public = issuing_keypair.public_key
    sender_secret = Account.get(Account.type == 'personal')
    source_key = Keypair.from_secret(sender_secret.secret)
    destination_id = to
    try:
        server.load_account(destination_id)
    except NotFoundError:
        raise Exception("The destination account does not exist!")
    source_account = server.load_account(source_key.public_key)
    base_fee = server.fetch_base_fee()
    transaction = (
        TransactionBuilder(
            source_account=source_account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=base_fee,
        )
        .append_payment_op(destination=destination_id, amount=amount, asset_code=asset_name, asset_issuer=issuing_public)
        .add_text_memo(memo)
        .set_timeout(10)
        .build()
    )

    transaction.sign(source_key)
    try:
        response = server.submit_transaction(transaction)
        return True
    except (BadRequestError, BadResponseError) as err:
        print(f"Something went wrong!\n{err}")
        return False