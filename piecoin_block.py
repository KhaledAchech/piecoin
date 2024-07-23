import datetime as date
import hashlib as hasher

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_bloc()
    
    def hash_bloc(self):
        sha = hasher.sha256()
        to_hash = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        sha.update(to_hash.encode())
        
        return sha.hexdigest()

def create_genesis_block():
    return Block(0, date.datetime.now(), "Genesis Block", "0")
    
def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    this_data = "Hey! I'm block " + str(this_index)
    this_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_hash)

blockchain = [create_genesis_block()]
previous_block = blockchain[0]

for i in range(20):
    block_to_add = next_block(previous_block)
    blockchain.append(block_to_add)
    previous_block = block_to_add
    print ("Block #{} has been added to the blockchain!".format(block_to_add.index))
    print ("Hash: {}\n".format(block_to_add.hash))

from flask import Flask, json
from flask import request
node = Flask(__name__)

this_nodes_transactions = []

@node.route('/txion', methos=['POST'])
def transaction():
    if request.method == 'POST':
        new_txion = request.get_json()
        this_nodes_transactions.append(new_txion)

        print("New transaction")
        print("FROM: {}".format(new_txion['from']))
        print("TO: {}".format(new_txion['to']))
        print("AMOUNT: {}\n".format(new_txion['amount']))

        return "Transaction submitted successfully\n"

node.run()

miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"

def proof_of_work(last_proof):
    incrementor = last_proof + 1

    while not(incrementor % 7 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    
    return incrementor

@node.route('/mine', methods = ['GET'])
def mine():
    last_block = blockchain[-1]
    last_proof = last_block.data['proof-of-work']

    proof = proof_of_work(last_proof)

    this_nodes_transactions.append(
        {"from": "network", "to": miner_address, "amount": 1}
    )

    new_block_data = {
        "proof_of_work": proof,
        "transactions": list(this_nodes_transactions)
    }
    new_block_index = last_block.index + 1
    new_block_timestamp = this_timestamp = date.datetime.now()
    last_block_hash = last_block.hash

    this_nodes_transactions = []

    mined_block = Block(
        new_block_index,
        new_block_timestamp,
        new_block_data,
        last_block_hash
    )
    blockchain.append(mined_block)

    return json.dumps({
        "index": new_block_index,
        "timestamp": str(new_block_timestamp),
        "data": new_block_data,
        "hash": last_block_hash
    }) + "\n"
    
@node.route('blocks', methods=['GET'])
def get_blocks():
    chain_to_send = blockchain

    for block in chain_to_send:
        block_index = str(block_index)
        block_timestamp = str(block.timestamp)
        block_data = str(block_data)
        block_hash = block_hash
        block = {
            "index": block_index,
            "timestamp": block_timestamp,
            "data": block_data,
            "hash": block_hash
        }
    
    chain_to_send = json.dumps(chain_to_send)
    return chain_to_send

def find_new_chain():
    other_chains = []
    for node_url in peer_nodes:
        block = request.get(node_url + "/blocks").content
        block = json.loads(block)
        other_chains.append(block)
    return other_chains

def consensus():
    other_chains = find_new_chain()
    longest_chain = blockchain
    for chain in other_chains:
        if (longest_chain < len(chain)):
            longest_chain = chain
    
    blockchain = longest_chain
