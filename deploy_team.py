# create_team.py

from utils import create_account, w3, Web3
import json
import time

def create_owner(password=None):
    address, key = create_account(password)

    data = {
        'address': address,
        'password': password,
        'key': key
    }

    with open('Owner.json', 'w') as outfile:
        json.dump(data, outfile)

    return address

def create_beneficiary(password=None):
    address, key = create_account(password)

    data = {
        'address': address,
        'password': password,
        'key': key
    }

    with open('Beneficiary.json', 'w') as outfile:
        json.dump(data, outfile)

    return address

def create_denis(password=None):
    address, key = create_account(password)

    data = {
        'address': address,
        'password': password,
        'key': key
    }

    with open('Denis.json', 'w') as outfile:
        json.dump(data, outfile)

    return address

def create_william(password=None):
    address, key = create_account(password)

    data = {
        'address': address,
        'password': password,
        'key': key
    }

    with open('William.json', 'w') as outfile:
        json.dump(data, outfile)

    return address

def create_matt(password=None):
    address, key = create_account(password)

    data = {
        'address': address,
        'password': password,
        'key': key
    }

    with open('Matt.json', 'w') as outfile:
        json.dump(data, outfile)

    return address

def create_user(password=None):
    address, key = create_account(password)

    data = {
        'address': address,
        'password': password,
        'key': key
    }

    with open('User.json', 'w') as outfile:
        json.dump(data, outfile)

    return address


def check(address=None, name=None):

    balance = w3.eth.getBalance(address)
    balance = Web3.fromWei(balance, 'ether')
    print('%s Account Eth Balance: %s' % (name, balance))

def send(user_address=None, owner_address=None, owner_key=None):
    try:
        gas_price = w3.eth.gasPrice
        block = w3.eth.getBlock("latest")
        gas_limit = block["gasLimit"]

        nonce = w3.eth.getTransactionCount(owner_address)

        _value = Web3.toWei(1000, 'ether')

        transaction = {
            'nonce': nonce,
            'gasPrice': gas_price,
            'gas': gas_limit,
            'chainId': None,
            'to': user_address,
            'value': _value
        }

        signed = w3.eth.account.signTransaction(transaction, owner_key)

        tx_hex = Web3.toHex(signed.rawTransaction)

        tx_hash = w3.eth.sendRawTransaction(tx_hex)

        while w3.eth.getTransactionReceipt(tx_hash) == None:
            time.sleep(5)
            print('Waiting on Tranasaction')

        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

        print(tx_receipt)

    except Exception as e:
        print('Error Sending Transaction: %s' % e)