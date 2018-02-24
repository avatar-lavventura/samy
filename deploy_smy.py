

import json
import time

from utils import w3, Web3, compile_files, decrypt_account

# SAMY Token Contract
# TODO
# [START SAMY Token Contract]
samy_compiled_sol = compile_files(['contracts/SamyToken.sol'])
samy_contract_interface = samy_compiled_sol['contracts/SamyToken.sol:SamyToken']
samy_contract = w3.eth.contract(abi=samy_contract_interface['abi'], bytecode=samy_contract_interface['bin'])

_initialSupply = 1000000000

# [END SAMY Token Contract]

# Deploy Samy Contract
# TODO
# [START Deploy Samy Contract]
def deploy_samy(owner_address=None, owner_key=None):

    try:

        gas_price = w3.eth.gasPrice
        block = w3.eth.getBlock("latest")
        gas_limit = block["gasLimit"] - 30000

        nonce = w3.eth.getTransactionCount(owner_address)

        built_transaction = {
            'nonce': nonce,
            'gasPrice': gas_price,
            'gas': gas_limit,
            #'chainId': None - SamyNet
            'chainId': 3
        }

        transaction = samy_contract.constructor().buildTransaction(built_transaction)

        signed = w3.eth.account.signTransaction(transaction, owner_key)

        tx_hex = Web3.toHex(signed.rawTransaction)

        tx_hash = w3.eth.sendRawTransaction(tx_hex)
        print(Web3.toHex(tx_hash))

        while w3.eth.getTransactionReceipt(tx_hash) == None:
            time.sleep(5)
            print('Waiting on Tranasaction')

        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

        contract_address = tx_receipt['contractAddress']

        data = {
            'address': contract_address
        }

        with open('SMYToken.json', 'w') as outfile:
            json.dump(data, outfile)

        return contract_address

    except Exception as e:
        print('Error Deploying SMY Token Contract; Error: %s', e)


# [END Deploy Samy Contract]


# Check Samy Contract
# TODO
# [START Check Samy Contract]
def check_samy(samy_token_address=None, address=None, name=None):

    try:

        samy_token_contract_instance = w3.eth.contract(samy_token_address, abi=samy_contract_interface['abi'])

        balance = samy_token_contract_instance.functions.balanceOf(address).call()
        balance = Web3.fromWei(balance, 'ether')
        print('%s Account SMY Token Balance: %s' % (name, balance))

        balance = w3.eth.getBalance(address)
        balance = Web3.fromWei(balance, 'ether')
        print('%s Account Eth Balance: %s' % (name, balance))

    except Exception as e:
        print('Error Checking SMY Token Contract; Error: %s', e)


# [END Check Samy Contract]

# Change Samy Contract Status
# TODO
# [START Change Samy Contract Status]
def check_status(smy_token_address=None, owner_address=None, owner_key=None):

    try:

        samy_token_contract_instance = w3.eth.contract(smy_token_address, abi=samy_contract_interface['abi'])

        return samy_token_contract_instance.functions.isActive().call()


    except Exception as e:
        print('Error Checking SMY Token Contract; Error: %s', e)

# [END Change Samy Contract Status]

# Change Samy Contract Status
# TODO
# [START Change Samy Contract Status]
def change_status(smy_token_address=None, owner_address=None, owner_key=None):

    try:

        samy_token_contract_instance = w3.eth.contract(smy_token_address, abi=samy_contract_interface['abi'])

        isActive = samy_token_contract_instance.functions.isActive().call()

        if isActive == False:

            gas_price = w3.eth.gasPrice * 2
            block = w3.eth.getBlock("latest")
            gas_limit = block["gasLimit"] - 30000

            nonce = w3.eth.getTransactionCount(owner_address)

            built_transaction = {
                'nonce': nonce,
                'gasPrice': gas_price,
                'gas': gas_limit,
                'chainId': 3
            }

            transaction = samy_token_contract_instance.functions.start().buildTransaction(built_transaction)

            signed = w3.eth.account.signTransaction(transaction, owner_key)

            tx_hex = Web3.toHex(signed.rawTransaction)

            tx_hash = w3.eth.sendRawTransaction(tx_hex)
            print(Web3.toHex(tx_hash))

            while w3.eth.getTransactionReceipt(tx_hash) == None:
                time.sleep(5)
                print('Waiting on Tranasaction')

            tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

            print('SMY Token is Active %s' % tx_receipt)

    except Exception as e:
        print('Error Checking SMY Token Contract; Error: %s', e)

# [END Change Samy Contract Status]
