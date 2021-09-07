import click
from stellar_sdk.server import Server
from .payment import new_payment
from beautifultable import BeautifulTable
from beautifultable import BTColumnCollection
from pygments.console import colorize
from .models import Account
from .asset import create_new_asset, issue_asset

server = Server(horizon_url="https://horizon-testnet.stellar.org")

@click.command()
@click.option('--to',prompt=f"Destination account public key\n{colorize('blue','run stellar-cli get-personal-accounts for a test account')}", help='The account you want to make a payment to')
@click.option('--memo',prompt="Enter a memo (reference)", help='A sort of reference number')
@click.option('--amount',prompt="Enter an amount to pay", help='The amount you want to pay')
@click.option('--asset',prompt="Enter an asset code", help='The asset code you want to send')
def make_payment(to, memo, amount, asset):
    click.echo(colorize('blue',"Making payment..."))
    payment_result = new_payment(to, memo, amount,asset)
    if payment_result:
        click.echo(colorize("green","Payment successful! run stellar-cli get-balances to view balances"))

@click.command()
def get_balances():
    all_accounts = Account.select()
    table = BeautifulTable()
    table.columns.header = ['Account Type','Public Key','Asset Type','Asset Code','Balance']
    for single_account in all_accounts:
        accounts = server.accounts().account_id(single_account.public).call()
        for balance in accounts['balances']:
            if "asset_code" in balance:
                table.rows.append([single_account.type,single_account.public,balance['asset_type'],balance['asset_code'],balance['balance']])
            else:
                table.rows.append([single_account.type,single_account.public,balance['asset_type'],None,balance['balance']])
    click.echo(table)

@click.command()
@click.option('--asset_name', prompt="Choose a name for your asset", help='The name of your asset')
def create_asset(asset_name):
    click.echo(colorize("green",f"Creating {asset_name} asset..."))
    transaction_resp = create_new_asset(asset_name)
    click.echo(colorize("blue",str(transaction_resp)))
    click.echo(colorize("green",f"Asset created successfully"))
    click.echo(colorize("green",f"Issuing assets to personal accounts. This may take a while depending on stellar network conditions."))
    asset_issued_hash = issue_asset(asset_name)
    click.echo(colorize("blue",str(asset_issued_hash)))
    click.echo(colorize("green",f"Assets issued successfully"))

@click.command()
def list_accounts():
    click.echo(colorize("green","Here are you current accounts"))
    table = BeautifulTable()
    table.columns.header = Account._meta.sorted_field_names
    all_accounts = Account.select().dicts()
    for a in all_accounts:
        table.rows.append(list(a.values()))
    click.echo(table)

@click.command()
def get_personal_accounts():
    for count,account in enumerate(Account.select().where(Account.type == 'personal')):
        if count == 0:
            click.echo(f"{colorize('red', 'PRIMARY ACCOUNT')}: {colorize('green',account.public)}")
        else:
            click.echo(f"{colorize('red', 'SECONDARY ACCOUNT (For testing)')}: {colorize('green',account.public)}")

