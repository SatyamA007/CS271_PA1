
from http import server
import socket
from collections import deque
from pickle import dumps, loads

def balanceInquire(user="1"):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(server_addr)
    transaction = {
        'type': 'balance',
        'from': user
    }
    data = {
        'sender': 'frontend_request',
        'transaction': transaction
    }
    transaction = dumps(data)
    server.sendall(transaction)
    buffer = loads(server.recv(1024))
    server.close()
    return buffer

def send_data(rcvr, data):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if rcvr == 'server':
        client_addr = server_addr
    else:
        client_addr = clients[int(rcvr) - 1]
    client.connect(client_addr)
    operation = dumps(data)
    client.sendall(operation)
    client.close()

initialBalance = 10

server_addr = ("127.0.0.1", 1234)
client1_addr = ("127.0.0.1", 1235)
client2_addr = ("127.0.0.1", 1236)
client3_addr = ("127.0.0.1", 1237)
clients = [client1_addr, client2_addr, client3_addr]

