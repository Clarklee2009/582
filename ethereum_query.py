from web3 import Web3
from hexbytes import HexBytes

IP_ADDR='18.188.235.196'
PORT='8545'

w3 = Web3(Web3.HTTPProvider('http://' + IP_ADDR + ':' + PORT))

# if w3.isConnected():
# #     This line will mess with our autograders, but might be useful when debugging
#     # print( "Connected to Ethereum node" )
# else:
#     print( "Failed to connect to Ethereum node!" )

def get_transaction(tx):
    tr = w3.eth.get_transaction(tx)  #YOUR CODE HERE
    return tr

# Return the gas price used by a particular transaction,
#   tx is the transaction
def get_gas_price(tx):
    tr = get_transaction(tx)
    gas_price = tr.gasPrice #YOUR CODE HERE
    return gas_price

def get_gas(tx):
    tr = w3.eth.get_transaction_receipt(tx)
    gas = tr.gasUsed
    return gas

def get_transaction_cost(tx):
    used = get_gas(tx)
    price = get_gas_price(tx)
    tx_cost = used * price
    return tx_cost

def get_block_cost(block_num):
    block_cost = 0  #YOUR CODE HERE
    bl = w3.eth.get_block(block_num)
    for tr in bl.transactions:
        block_cost += get_transaction_cost(tr)
    return block_cost

# Return the hash of the most expensive transaction
def get_most_expensive_transaction(block_num):
    m = 0  #YOUR CODE HERE
    bl = w3.eth.get_block(block_num)
    for tr in bl.transactions:
        if get_transaction_cost(tr) > m:
            m = get_transaction_cost(tr)
    max_tx = HexBytes(m)  #YOUR CODE HERE
    return max_tx
