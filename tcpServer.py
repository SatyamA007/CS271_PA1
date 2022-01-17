import datetime
import socket
from pickle import dumps, loads
# Calculating the hash
# in order to add digital
# fingerprints to the blocks
import hashlib
 
# To store data
# in our blockchain
import json
 
# Flask is for creating the web
# app and jsonify is for
# displaying the blockchain
from flask import Flask, jsonify
 
 
class Blockchain:
   
    # This function is created
    # to create the very first
    # block and set it's hash to "0"
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')
 
    # This function is created
    # to add further blocks
    # into the chain
    def create_block(self, proof, previous_hash, data={'sndr':"sender", 'rcvr':"receiver", 'amt':"0"}):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'data': data}
        self.chain.append(block)
        return block
       
    # This function is created
    # to display the previous block
    def print_previous_block(self):
        return self.chain[-1]
       
    # This is the function for proof of work
    # and used to successfully mine the block
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
         
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1
                 
        return new_proof
 
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
 
    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
         
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
               
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()).hexdigest()
             
            if hash_operation[:5] != '00000':
                return False
            previous_block = block
            block_index += 1
         
        return True
        
 
 
# Creating the Web
# App using flask
app = Flask(__name__)
 
# Create the object
# of the class blockchain
blockchain = Blockchain()
initialBalance = 10

# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block(sndr='sndr', rcvr="receiver", amt="0"):
    data={'sndr':sndr, "rcvr":rcvr, "amt":amt}
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash, data)
     
    response = {'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'data':block['data']}
#    return jsonify(response), 200
 
# Display blockchain in json format
@app.route('/get_chain', methods=['GET'])
def display_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200
 
# Check validity of blockchain
@app.route('/valid', methods=['GET'])
def valid():
    valid = blockchain.chain_valid(blockchain.chain)
     
    if valid:
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return jsonify(response), 200
 
def balanceInquire(user="me"):
    chain = blockchain.chain
    block_index = 0
    sum = initialBalance

    while block_index < len(chain):
        block = chain[block_index]
             
        if block['data']['sndr'] == user:
            sum-=int(block['data']['amt'])
            
        elif block['data']['rcvr'] == user:
            sum+=int(block['data']['amt'])

        block_index += 1
        
    return sum

def sendMoney(sndr, rcvr, amt):
    balance = balanceInquire(sndr)
    if balance<int(amt):
        return "fail"
    else:
        mine_block(sndr,rcvr,amt)
        return "pass"
 
# Run the flask server locally
#app.run(host='127.0.0.1', port=5000)


if __name__=="__main__":
    ip = "127.0.0.1"
    port = 1234
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip,port))
    server.listen(5)
    blockchain = Blockchain()
    initialBalance = 10
    

    transaction = {
        'type': 'send_money',
        'from': '1',
        'to': '2',
        'amount': 5
    }
    data = {
        'sender': 'server_request',
        'transaction': transaction
    }
    while True:
        client,address = server.accept()
        
        print(f"Connection Established - {address[0]}, {address[1]}")
        
        send_data(transaction['from'], data)

        print(f"Connection Established - {address[0]}, {address[1]}")
        message = client.recv(1024).decode()
        
        args = loads(message)
        print(args)

        if args['transaction']['type'] == 'send_money':
            result = str.encode(sendMoney(args['from'], args['to'], args['amount']))
        elif args['transaction']['type'] == 'balance':
            result = str.encode(str(balanceInquire(args['from'])))
        send_data(args['from'], result)





