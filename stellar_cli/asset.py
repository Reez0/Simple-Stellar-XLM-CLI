from .models import Account
from stellar_sdk.asset import Asset
from stellar_sdk.keypair import Keypair
from stellar_sdk.network import Network
from stellar_sdk.server import Server
from stellar_sdk.transaction_builder import TransactionBuilder


def create_new_asset(asset_name):
    server = Server(horizon_url="https://horizon-testnet.stellar.org")
    network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
    issuing_keypair_secret = Account.get(Account.type == 'issuer').secret
    issuing_keypair = Keypair.from_secret(issuing_keypair_secret
    )
    issuing_public = issuing_keypair.public_key
    distributor_keypair_secret = Account.get(Account.type == 'distributor').secret
    distributor_keypair = Keypair.from_secret(distributor_keypair_secret)
    distributor_public = distributor_keypair.public_key
    distributor_account = server.load_account(distributor_public)
    new_asset = Asset(asset_name, issuing_public)
    trust_transaction = (
        TransactionBuilder(
            source_account=distributor_account,
            network_passphrase=network_passphrase,
            base_fee=100,
        )
        .append_change_trust_op(
            asset_code=new_asset.code, asset_issuer=new_asset.issuer, limit="1000"
        )
        .set_timeout(100)
        .build()
    )

    trust_transaction.sign(distributor_keypair)
    trust_transaction_resp = server.submit_transaction(trust_transaction)
    issuing_account = server.load_account(issuing_public)
    payment_transaction = (
        TransactionBuilder(
            source_account=issuing_account,
            network_passphrase=network_passphrase,
            base_fee=100,
        )
        .append_payment_op(
            destination=distributor_public,
            amount="1000",
            asset_code=new_asset.code,
            asset_issuer=new_asset.issuer,
        )
        .build()
    )
    payment_transaction.sign(issuing_keypair)
    payment_transaction_resp = server.submit_transaction(payment_transaction)
    return payment_transaction_resp

def issue_asset(asset_name):
    server = Server(horizon_url="https://horizon-testnet.stellar.org")
    network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
    admin_account = Account.get(Account.type == 'issuer').secret
    issuing_keypair = Keypair.from_secret(admin_account)
    issuing_public = issuing_keypair.public_key
    for account in Account.select().where(Account.type == 'personal'):
        distributor_keypair = Keypair.from_secret(account.secret)
        distributor_public = distributor_keypair.public_key
        distributor_account = server.load_account(distributor_public)
        new_asset = Asset(asset_name, issuing_public)
        trust_transaction = (
            TransactionBuilder(
                source_account=distributor_account,
                network_passphrase=network_passphrase,
                base_fee=100,
            )
            .append_change_trust_op(
                asset_code=new_asset.code, asset_issuer=new_asset.issuer
            )
            .set_timeout(100)
            .build()
        )

        trust_transaction.sign(distributor_keypair)
        trust_transaction_resp = server.submit_transaction(trust_transaction)
        issuing_account = server.load_account(issuing_public)
        # Second, the issuing account actually sends a payment using the asset.
        payment_transaction = (
            TransactionBuilder(
                source_account=issuing_account,
                network_passphrase=network_passphrase,
                base_fee=100,
                
            )
            .append_payment_op(
                destination=distributor_public,
                amount="100",
                asset_code=new_asset.code,
                asset_issuer=new_asset.issuer,
            )
            .add_text_memo('Initial asset funds')
            .build()
        )
        payment_transaction.sign(issuing_keypair)
        payment_transaction_resp = server.submit_transaction(payment_transaction)
        import time
        time.sleep(5)
    return payment_transaction_resp['hash']