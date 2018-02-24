

import json
import time

from utils import w3, Web3, compile_files, decrypt_account

from deploy_smy import samy_contract_interface, _initialSupply

from datetime import datetime

# Crowdsale Contract
# TODO
# [START Crowdsale Contract]

crowdsale_compiled_sol = compile_files(['contracts/Crowdsale.sol'])
crowdsale_contract_interface = crowdsale_compiled_sol['contracts/Crowdsale.sol:Crowdsale']
crowdsale_contract = w3.eth.contract(abi=crowdsale_contract_interface['abi'],
                                     bytecode=crowdsale_contract_interface['bin'])

# [END Crowdsale Contract]

def deploy_crowdsale(smy_token_address=None, owner_address=None, owner_key=None, beneficiary_address=None):

    _rate = 10000 # 10,000 per 1 Eth

    _fundingGoal = .50 # 1,000,000 $USD
    _fundingGoal = Web3.toWei(_fundingGoal, 'ether')

    _bonus_start = int(time.time())
    _bonus_end = int(time.time() + 3600)
    _start_time = _bonus_end
    _end_time = int(_start_time + 86400)

    _bonus = 20 # 20% Bonus

    _cap = int(_initialSupply * .21) # 21 % Initial Supply
    _cap = Web3.toWei(_cap, 'ether')

    gas_price = w3.eth.gasPrice * 2
    block = w3.eth.getBlock("latest")
    gas_limit = block["gasLimit"] - 30000

    nonce = w3.eth.getTransactionCount(owner_address)

    built_transaction = {
        'nonce': nonce,
        'gasPrice': gas_price,
        'gas': gas_limit,
        #'chainId': None,
        'chainId': 3
    }

    transaction = crowdsale_contract.constructor(
        args=(
            beneficiary_address,
            _fundingGoal,
            _cap,
            _rate,
            _start_time,
            _end_time,
            _bonus_start,
            _bonus_end,
            _bonus,
            smy_token_address
        )
    ).buildTransaction(built_transaction)

    signed = w3.eth.account.signTransaction(transaction, owner_key)

    tx_hex = Web3.toHex(signed.rawTransaction)

    tx_hash = w3.eth.sendRawTransaction(tx_hex)
    print(Web3.toHex(tx_hash))
    startTime = time.time()
    while w3.eth.getTransactionReceipt(tx_hash) == None:
        time.sleep(5)
        print('Waiting on Tranasaction')

    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

    contract_address = tx_receipt['contractAddress']

    data = {
        'address': contract_address
    }

    with open('Crowdsale.json', 'w') as outfile:
        json.dump(data, outfile)

    print('Elapsed Time: %s' % (int(time.time()) - int(startTime)))

    return contract_address


def fund_crowdsale(smy_token_address=None, owner_address=None, owner_key=None, crowdsale_address=None):

    _amount = int(_initialSupply * .21) # 21% Initial Supply
    _amount = Web3.toWei(_amount, 'ether')

    try:

        crowdsale_contract_instance = w3.eth.contract(smy_token_address, abi=samy_contract_interface['abi'])

        gas_price = w3.eth.gasPrice * 2
        block = w3.eth.getBlock("latest")
        gas_limit = block["gasLimit"] - 30000

        nonce = w3.eth.getTransactionCount(owner_address)

        built_transaction = {
            'nonce': nonce,
            'gasPrice': gas_price,
            'gas': gas_limit,
            #'chainId': None,
            'chainId': 3
        }

        transaction = crowdsale_contract_instance.functions.transfer(crowdsale_address, _amount).buildTransaction(built_transaction)

        signed = w3.eth.account.signTransaction(transaction, owner_key)

        tx_hex = Web3.toHex(signed.rawTransaction)

        tx_hash = w3.eth.sendRawTransaction(tx_hex)

        print(Web3.toHex(tx_hash))
        startTime = time.time()

        while w3.eth.getTransactionReceipt(tx_hash) == None:
            time.sleep(5)
            print('Waiting on Tranasaction')

        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

        print('Crowdsale Funded with SMY: %s' % tx_receipt)

        print('Elapsed Time: %s' % (int(time.time()) - int(startTime)))

    except Exception as e:
        print('Error Funding Crowdsale Contract: %s' % e)

def check_crowdsale(smy_token_address=None, crowdsale_address=None):

    samy_token_contract_instance = w3.eth.contract(smy_token_address, abi=samy_contract_interface['abi'])
    crowdsale_contract_instance = w3.eth.contract(crowdsale_address, abi=crowdsale_contract_interface['abi'])

    refund_vault_address = crowdsale_contract_instance.functions.vault().call()

    print('Current Time %s' % time.time())
    print('Crowdsale Bonus Start Time %s' % crowdsale_contract_instance.functions.bonusStart().call())
    print('Crowdsale Bonus End Time %s' % crowdsale_contract_instance.functions.bonusEnd().call())
    print('Crowdsale Start Time %s' % crowdsale_contract_instance.functions.startTime().call())
    print('Crowdsale End Time %s' % crowdsale_contract_instance.functions.endTime().call())
    amountRaised = crowdsale_contract_instance.functions.weiAmountRaised().call()
    amountRaised = Web3.fromWei(amountRaised, 'ether')
    print('Crowdsale Amount Raised %s' % amountRaised)
    fundingGoal = crowdsale_contract_instance.functions.fundingGoal().call()
    fundingGoal = Web3.fromWei(fundingGoal, 'ether')
    print('Crowdsale Funding Goal %s' % fundingGoal)
    goal_reached = crowdsale_contract_instance.functions.goalReached().call()
    has_ended = crowdsale_contract_instance.functions.hasEnded().call()
    print('Crowdsale Has Ended: %s' % has_ended)
    print('Crowdsale Goal Reached: %s' % goal_reached)
    print('Crowdsale Beneficiary Address %s' % crowdsale_contract_instance.functions.beneficiary().call())

    rate = crowdsale_contract_instance.functions.rate().call()
    print('Crowdsale Tokens per 1 Ether: %s' % rate)

    smyBalance = samy_token_contract_instance.functions.balanceOf(crowdsale_address).call()
    smyBalance = Web3.fromWei(smyBalance, 'ether')
    if smyBalance == 0:
        return False

    print('Crowdsale Contract Balance of SMY Tokens: %s' % smyBalance)
    ethBalance = w3.eth.getBalance(refund_vault_address)
    ethBalance = Web3.fromWei(ethBalance, 'ether')
    print('Vault Contract Balance of Ether: %s' % ethBalance)

    return has_ended, goal_reached

def transaction_crowdsale(crowdsale_address=None, user_address=None, user_key=None):

    try:
        gas_price = w3.eth.gasPrice * 2
        block = w3.eth.getBlock("latest")
        gas_limit = block["gasLimit"] - 30000

        nonce = w3.eth.getTransactionCount(user_address)

        _value = Web3.toWei(.25, 'ether')

        transaction = {
            'nonce': nonce,
            'gasPrice': gas_price,
            'gas': gas_limit,
            #'chainId': None,
            'chainId': 3,
            'to': crowdsale_address,
            'value': _value
        }

        signed = w3.eth.account.signTransaction(transaction, user_key)

        tx_hex = Web3.toHex(signed.rawTransaction)

        tx_hash = w3.eth.sendRawTransaction(tx_hex)
        print(Web3.toHex(tx_hash))
        startTime = time.time()

        while w3.eth.getTransactionReceipt(tx_hash) == None:
            time.sleep(5)
            print('Waiting on Tranasaction')

        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

        print('Crowdsale Transaction: %s' % tx_receipt)
        print('Elapsed Time: %s' % (int(time.time()) - int(startTime)))

    except Exception as e:
        print('Error Sending Transaction: %s' % e)


def finalize_crowdsale(crowdsale_address=None, owner_address=None, owner_key=None):

    crowdsale_contract_instance = w3.eth.contract(crowdsale_address, abi=crowdsale_contract_interface['abi'])

    gas_price = w3.eth.gasPrice
    block = w3.eth.getBlock("latest")
    gas_limit = block["gasLimit"]

    nonce = w3.eth.getTransactionCount(owner_address)

    built_transaction = {
        'nonce': nonce,
        'gasPrice': gas_price,
        'gas': gas_limit,
        #'chainId': None,
        'chainId': 3
    }

    transaction = crowdsale_contract_instance.functions.finalization().buildTransaction(
        built_transaction)

    signed = w3.eth.account.signTransaction(transaction, owner_key)

    tx_hex = Web3.toHex(signed.rawTransaction)

    tx_hash = w3.eth.sendRawTransaction(tx_hex)
    print(Web3.toHex(tx_hash))
    startTime = time.time()

    while w3.eth.getTransactionReceipt(tx_hash) == None:
        time.sleep(5)
        print('Waiting on Tranasaction')

    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

    print('Crowdsale Finalization: %s' % tx_receipt)

    finalized = crowdsale_contract_instance.functions.isFinalized().call()

    print('Crowdsale is finalized: %s' % finalized)
    print('Elapsed Time: %s' % (int(time.time()) - int(startTime)))


def refund_crowdsale(crowdsale_address=None, owner_address=None, owner_key=None):

    crowdsale_contract_instance = w3.eth.contract(crowdsale_address, abi=crowdsale_contract_interface['abi'])

    gas_price = w3.eth.gasPrice * 2
    block = w3.eth.getBlock("latest")
    gas_limit = block["gasLimit"] - 50000

    nonce = w3.eth.getTransactionCount(owner_address)

    built_transaction = {
        'nonce': nonce,
        'gasPrice': gas_price,
        'gas': gas_limit,
        #'chainId': None,
        'chainId': 3
    }

    transaction = crowdsale_contract_instance.functions.sendRefunds().buildTransaction(
        built_transaction)

    signed = w3.eth.account.signTransaction(transaction, owner_key)

    tx_hex = Web3.toHex(signed.rawTransaction)

    tx_hash = w3.eth.sendRawTransaction(tx_hex)
    print(Web3.toHex(tx_hash))
    startTime = time.time()

    while w3.eth.getTransactionReceipt(tx_hash) == None:
        time.sleep(5)
        print('Waiting on Tranasaction')

    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

    print('Crowdsale Refunded: %s' % tx_receipt)
    print('Elapsed Time: %s' % (int(time.time()) - int(startTime)))

def get_contributions(crowdsale_address=None):
    try:
        crowdsale_contract_instance = w3.eth.contract(crowdsale_address, abi=crowdsale_contract_interface['abi'])
        all_filter = crowdsale_contract_instance.eventFilter('TokenContribution', {'fromBlock': 0, 'toBlock': 'latest'})
        all_contributions = all_filter.get_all_entries()
        for contribution in all_contributions:
            print(contribution)
    except Exception as e:
        print('Error Getting Token Contributions: %s' % e)


def get_finalization(crowdsale_address=None):
    try:
        crowdsale_contract_instance = w3.eth.contract(crowdsale_address, abi=crowdsale_contract_interface['abi'])
        all_filter = crowdsale_contract_instance.eventFilter('Finalization', {'fromBlock': 0, 'toBlock': 'latest'})
        all_finalizations = all_filter.get_all_entries()
        for finalization in all_finalizations:
            print(finalization)
    except Exception as e:
        print('Error Getting Token Finalization: %s' % e)

def get_test(crowdsale_address=None):
    try:
        crowdsale_contract_instance = w3.eth.contract(crowdsale_address, abi=crowdsale_contract_interface['abi'])
        all_filter = crowdsale_contract_instance.eventFilter('Test', {'fromBlock': 0, 'toBlock': 'latest'})
        all_tests = all_filter.get_all_entries()
        for test in all_tests:
            print(test)
    except Exception as e:
        print('Error Getting Token Finalization: %s' % e)
