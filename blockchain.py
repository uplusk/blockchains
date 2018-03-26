import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request

#creating our class
class Blockchain(object):
    
    def __init__(self):
        self.current_transaction = []
        self.chain = []
        self.nodes = set()
        
        #To create a Genesis block
        self.new_block(previous_hash='1', proof=10)
       

    #register new nodes on your network
    def register_node(self,address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    #here address is the parsed address of the node you're trying to register

    #to check the validity of your blockchain when trying to add a new block/participating in consensus
    def valid_chain(self,chain):
        last_block = chain[0]

        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')

            #check previous hash
            if block['previous_hash'] != self.hash(last_block):
                return False
            
            #check proof of work
            if not self.valid_proof(last_block['proof'],block['proof'],block['previous_hash']):
                return False


            last_block = block
            current_index +=1

        return True

    #it checks if the length of your chain is smaller than the chain of the nodes in your network
    def consensus(self):
        neighbors = self.nodes
        new_chain = None

        #We're finding chains longer than ours
        max_length = len(self.chain)
        for node in neighbors:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    #Replace if the chain is longer than yours
                    max_length = length
                    new_chain = chain
        if new_chain:
            self.chain = new_chain
            return True
        
        return False

    #adding a new block post mining 
    def new_block(self,proof,previous_hash=None):
      #Adds a new block to the existing ledger  
        block = {
            'index' : len(self.chain) +1,
            'timestamp': time(),
            'proof': proof,
            'previous_hash': previous_hash,
            'transactions': self.current_transaction
        }
        
        #Reset the transaction list
        self.current_transaction = []
        
        self.chain.append(block)
        return block

     
    def new_transaction(self,sender,recipient,amount):
        #Adds a new transaction to be validated
        self.current_transaction.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        
        self.last_block['index'] +1
        
        
        
    @staticmethod
    def hash(block):
        #Computes the hash of the block for identification
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
        
    @property
    def last_block(self):
        #The last block of the ledger, gives the present state of the ledger
        return self.chain[-1]

   
    def proof_of_work(self,last_block):
        last_proof = last_block['proof']
        last_hash = self.hash(last_block)
        
        proof = 0
        while self.valid_proof(last_proof,proof,last_hash) is False:
            proof +=1
            
        return proof
    
    @staticmethod
    def valid_proof(last_proof,proof,last_hash):
        spec = f'{last_proof}{proof}{last_hash}'.encode()
        spec_hash = hashlib.sha256(spec).hexdigest()
        return spec_hash[:4] == '2020'



app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

#instantiate the class
blockchain = Blockchain()

@app.route('/',methods=['GET'])
def index():
    return "Blockchain API's"


@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    
    
    proof = blockchain.proof_of_work(last_block)
    #The reward for finding the proof is a new transaction from sender 0 and recipient is our node identifier
    blockchain.new_transaction(sender="0", recipient=node_identifier,amount=1)
    
    #New Block is forged by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof,previous_hash)
    
    return jsonify({
        'message': 'New Block forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': previous_hash
    }), 200


#api to add a new transaction
@app.route('/transactions/new',methods=['POST'])
def new_transaction():
    body = request.get_json()
    
    #sends back an error if values are missing
    required = ['sender','recipient','amount']
    if not all(k in body for k in required):
        return 'Values Missing', 400
    
    trans = blockchain.new_transaction(body['sender'],body['recipient'],body['amount'])
    response = {'message': f'New transaction will be added to block {trans}'}
    
    return jsonify(response), 201

#api for the consensus mechanism
@app.route('/nodes/consensus', methods=['GET'])
def consensus():
    new_chain = blockchain.consensus()
    if new_chain:
        response = {
            'message': 'Your chain was replaced',
            'chain':blockchain.chain
        }
    else:
        response = {
            'message': 'Your chain is authoritative',
            'chain': blockchain.chain
        }
    return jsonify(response),200

#api to register the node
@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

#api to get the full ledger
@app.route('/chain',methods=['GET'])
def full_chain():
    chain = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    
    return jsonify(chain), 200

if __name__ == '__main__':
    app.run(port=5000)