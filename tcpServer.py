
import socket
import socketio
from pickle import dumps, loads
# Calculating the hash
# in order to add digital
# fingerprints to the blocks

 
# To store data
# in our blockchain
from blockchain import *
from util import *
# Flask is for creating the web
# app and jsonify is for
# displaying the blockchain
from flask import Flask, jsonify
 
# Creating the Web
# App using flask
app = Flask(__name__)
 
# Create the object
# of the class blockchain
blockchain = Blockchain()

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
 
def getBalance(user="me"):
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


def makeTransaction(sndr, rcvr, amt):
    balance = getBalance(sndr)
    if balance<int(amt):
        return "fail"
    else:
        mine_block(sndr,rcvr,amt)
        return "pass"
 
# Run the flask server locally
#app.run(host='127.0.0.1', port=5000)

def inform_front_end(sio_frontEnd, event ,message):
    try:
        sio_frontEnd.connect("http://127.0.0.1:5000")
    except:
        print("Front-end already connected")

    sio_frontEnd.emit(event, message)

if __name__=="__main__":
    ip = "127.0.0.1"
    port = 1234
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip,port))
    server.listen(max_tcp_connections)
    blockchain = Blockchain()
    
    sio_frontEnd = socketio.Client()
  
    while True:
        client,address = server.accept()
        
        print(f"Connection Established - {address[0]}, {address[1]}")
        
        message = client.recv(1024)
        
        args = loads(message)
        transaction = args['transaction']
        if transaction['type'] == 'send_money':
            result = makeTransaction(transaction['from'], transaction['to'], transaction['amount'])
            data = {
                'sender': 'server_reply',
                'result': result
            }
            send_data(transaction['from'], data)
            inform_front_end(sio_frontEnd,'send_money_result', {'data':[transaction['from'], transaction['to'], transaction['amount']],'result': result})
        elif transaction['type'] == 'balance':
            amt = str(getBalance(transaction['from']))
            data = {
                'sender': 'server_reply',
                'result': amt
            }
            send_data(transaction['from'], data)
            inform_front_end(sio_frontEnd,'balance_inquiry_result', {'data':transaction['from'], 'amt': amt})
            




