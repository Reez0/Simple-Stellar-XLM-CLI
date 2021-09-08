# Stellar XLM CLI

A command line tool for interacting with the Stellar XLM API and the Stellar XLM SDK.

## Installation

Clone or download the repository

```bash
python3 pip install -r requirements.txt
```

## Usage

1. Create new accounts by running the command `python3 -m stellar-cli`. Four accounts will be created as well as an SQLite3 database.

2. Create your asset

Create your new tokenized asset by running 
`python3 -m stellar-cli create-asset`
You will be prompted for a name for your asset.

3. Make a payment

Make a payment to another account using `python3 -m stellar-cli make-payment` and follow the prompts. For an account to test sending payments of your assets to, you can use `python3 -m stellar-cli get-personal-accounts`. By default, the first account created with the `personal` flag will be your primary account.

4. Get balances

You can view balances of your account using `python3 -m stellar-cli get-balances`. This will list the balances of all accounts.

5.If you would like to see a list of all accounts contained in `accounts.db`, you can use `python3 -m stellar-cli list-accounts`