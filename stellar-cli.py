from peewee import SqliteDatabase
from stellar_cli import account
from stellar_cli.models import Account
import os
import click
from pygments.console import colorize
from stellar_cli.commands import make_payment, get_balances, create_asset, list_accounts, get_personal_accounts
from stellar_cli.payment import new_payment

database = SqliteDatabase('accounts.db')

def create_tables():
    with database:
        database.create_tables([Account])

@click.group()
def stellar_cli():
    pass

stellar_cli.add_command(make_payment)
stellar_cli.add_command(get_balances)
stellar_cli.add_command(create_asset)
stellar_cli.add_command(list_accounts)
stellar_cli.add_command(get_personal_accounts)

if __name__ == "__main__":
    if not os.path.exists('accounts.db'):
        create_tables()
        with database as db:
            account_types = ['distributor','issuer','personal','personal']
            for count, account_type in enumerate(account_types, start=1):
                account_created = account.create_account(db, account_type)
                if account_created:
                    print(colorize("green", f"Account {count} created successfully"))
            print(colorize("green","Funding accounts... Please wait."))
            for user_account in Account.select():
                account_funded =account.fund_account(user_account)
                    
    else:
        stellar_cli()

