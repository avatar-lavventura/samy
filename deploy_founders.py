

import json
import time

from utils import w3, Web3, compile_files, decrypt_account

from deploy_smy import samy_contract_interface, _initialSupply

from datetime import datetime

# Founder Token Contract
# TODO
# [START Founder Token Contract]
founder_compiled_sol = compile_files(['contracts/TokenVesting.sol'])  # Compiled source code
founder_contract_interface = founder_compiled_sol['contracts/TokenVesting.sol:TokenVesting']
founder_contract = w3.eth.contract(abi=founder_contract_interface['abi'], bytecode=founder_contract_interface['bin'])


# [END Founder Token Contract]

# Deploy Founders Contract
# TODO
# [START Deploy Founders Contract]
def deploy_founders(owner_address=None, owner_key=None, founders=None):

    try:
        founder_list = []
        i = 0
        for founder in founders:
            i += 1
            try:
                _beneficiary = founder['address']
                _start = int(time.time())
                _cliff = int(60)
                _duration = int(120)
                _revocable = True

                gas_price = w3.eth.gasPrice
                block = w3.eth.getBlock("latest")
                gas_limit = block["gasLimit"]

                nonce = w3.eth.getTransactionCount(owner_address)

                built_transaction = {
                    'nonce': nonce,
                    'gasPrice': gas_price,
                    'gas': gas_limit,
                    'chainId': None
                }


                transaction = founder_contract.constructor(args=(_beneficiary,
                                                        _start,
                                                        _cliff,
                                                        _duration,
                                                        _revocable),
                ).buildTransaction(built_transaction)

                signed = w3.eth.account.signTransaction(transaction, owner_key)

                tx_hex = Web3.toHex(signed.rawTransaction)

                tx_hash = w3.eth.sendRawTransaction(tx_hex)

                while w3.eth.getTransactionReceipt(tx_hash) == None:
                    time.sleep(5)
                    print('Waiting on Tranasaction')

                tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

                contract_address = tx_receipt['contractAddress']

                print('Founder {} Contract Address: {}'.format(founder['name'], contract_address))

                data = {
                    'name': '%s' % founder['name'],
                    'address': contract_address
                }
                founder_list.append(data)

            except Exception as e:
                print('Error Deploying Founder %s Contract: %s' % (founder['name'], e))
                break

        with open('Founders.json', 'w') as outfile:
            json.dump(founder_list, outfile)

    except Exception as e:
        print('Error Deploying Founder Contracts; Error: %s', e)


# [END Deploy Samy Contract]

# Fund Founders
# TODO
# [START Fund Founders]
def fund_founders(smy_token_address=None, owner_address=None, owner_key=None, founders=None):

    i = 0
    for founder in founders:
        try:
            i += 1

            print('Funding Founder %s' % founder['name'])

            _amount = int(_initialSupply * .05)
            _amount = Web3.toWei(_amount, 'ether')
            _amount = int(_amount / 3)

            samy_contract_instance = w3.eth.contract(smy_token_address, abi=samy_contract_interface['abi'])

            gas_price = w3.eth.gasPrice
            block = w3.eth.getBlock("latest")
            gas_limit = block["gasLimit"]

            nonce = w3.eth.getTransactionCount(owner_address)

            built_transaction = {
                'nonce': nonce,
                'gasPrice': gas_price,
                'gas': gas_limit,
                'chainId': None
            }

            transaction = samy_contract_instance.functions.transfer(founder['address'], _amount).buildTransaction(built_transaction)

            signed = w3.eth.account.signTransaction(transaction, owner_key)

            tx_hex = Web3.toHex(signed.rawTransaction)

            tx_hash = w3.eth.sendRawTransaction(tx_hex)

            while w3.eth.getTransactionReceipt(tx_hash) == None:
                time.sleep(5)
                print('Waiting on Tranasaction')

            tx_receipt = w3.eth.getTransactionReceipt(tx_hash)


        except Exception as e:
            print('Error Funding Founder %s; Error: %s' % (founder['name'], e))
            break

# [END Fund Founders]

# Check Founder Contract
# TODO
# [START Check Founder Contract]
def check_founders(smy_token_address=None, founders=None):

    i = 0
    for founder in founders:

        samy_contract_instance = w3.eth.contract(smy_token_address, abi=samy_contract_interface['abi'])

        founder_contract_instance = w3.eth.contract(founder['address'], abi=founder_contract_interface['abi'])

        start = founder_contract_instance.functions.start().call()
        start_date = datetime.fromtimestamp(float(start)).strftime('UTC-%Y-%m-%dT%H-%M-%S.%fZ')
        cliff = founder_contract_instance.functions.cliff().call()
        cliff_date = datetime.fromtimestamp(float(cliff)).strftime('UTC-%Y-%m-%dT%H-%M-%S.%fZ')
        duration = founder_contract_instance.functions.duration().call() + start
        end_date = datetime.fromtimestamp(float(duration)).strftime('UTC-%Y-%m-%dT%H-%M-%S.%fZ')

        print('Current Datetime: %s' % datetime.fromtimestamp(float(time.time())).strftime('UTC-%Y-%m-%dT%H-%M-%S.%fZ'))

        print('Founder %s Contract Vesting Start Datetime: %s' % (founder['name'], start_date))
        print('Founder %s Contract Vesting Cliff Datetime: %s' % (founder['name'], cliff_date))
        print('Founder %s Contract Vesting End Datetime: %s' % (founder['name'], end_date))

        balance = samy_contract_instance.functions.balanceOf(founder['address']).call()
        balance = Web3.fromWei(balance, 'ether')
        print('Founder %s Contract SMY Token Balance: %s' % (founder['name'], balance))

        balance = founder_contract_instance.functions.releasableAmount(smy_token_address).call()
        balance = Web3.fromWei(balance, 'ether')
        print('Founder %s Contract Releaseable Amount: %s' % (founder['name'], balance))



# [END Check Samy Contract]


# Release Founders
# TODO
# [START Release Founders]
def release_founders(smy_token_address=None, owner_address=None, owner_key=None, founders=None):

    i = 0
    for founder in founders:
        try:

            i += 1

            founder_contract_instance = w3.eth.contract(founder['address'], abi=founder_contract_interface['abi'])

            gas_price = w3.eth.gasPrice
            block = w3.eth.getBlock("latest")
            gas_limit = block["gasLimit"]

            nonce = w3.eth.getTransactionCount(owner_address)

            built_transaction = {
                'nonce': nonce,
                'gasPrice': gas_price,
                'gas': gas_limit,
                'chainId': None
            }

            transaction = founder_contract_instance.functions.release(smy_token_address).buildTransaction(built_transaction)

            signed = w3.eth.account.signTransaction(transaction, owner_key)

            tx_hex = Web3.toHex(signed.rawTransaction)

            tx_hash = w3.eth.sendRawTransaction(tx_hex)

            while w3.eth.getTransactionReceipt(tx_hash) == None:
                time.sleep(5)
                print('Waiting on Tranasaction')

            tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

            print('Founder %s funds released; %s' % (founder['name'], tx_receipt))

        except Exception as e:
            print(e)
            break

# [END Release Founders]

# Revoke Founders
# TODO
# [START Revoke Founders]
def revoke_founders(smy_token_address=None, owner_address=None, owner_key=None, founders=None):

    i = 0
    for founder in founders:
        try:

            i += 1

            founder_contract_instance = w3.eth.contract(founder['address'], abi=founder_contract_interface['abi'])

            gas_price = w3.eth.gasPrice
            block = w3.eth.getBlock("latest")
            gas_limit = block["gasLimit"]

            nonce = w3.eth.getTransactionCount(owner_address)

            built_transaction = {
                'nonce': nonce,
                'gasPrice': gas_price,
                'gas': gas_limit,
                'chainId': None
            }

            transaction = founder_contract_instance.functions.revoke(smy_token_address).buildTransaction(
                built_transaction)

            signed = w3.eth.account.signTransaction(transaction, owner_key)

            tx_hex = Web3.toHex(signed.rawTransaction)

            tx_hash = w3.eth.sendRawTransaction(tx_hex)

            while w3.eth.getTransactionReceipt(tx_hash) == None:
                time.sleep(5)
                print('Waiting on Tranasaction')

            tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

            print('Founder %s funds revoked' % founder['name'])

        except Exception as e:
            print(e)
            break

# [END Revoke Founders]