
from http import server
import socket
from collections import deque
from pickle import dumps, loads

def balanceInquire(user="1"):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(server_addr)    
    transaction = str.encode("*".join(["balance", user, "receiver", "100"]) +"\n")
    server.sendall(transaction)
    buffer = server.recv(1024).decode()
    server.close()
    return buffer

def sendMoney(sndr="1", rcvr="2", amount="0"):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(server_addr)
    transaction = str.encode("*".join([str("send_money"), str(sndr), str(rcvr), str(amount)])+"\n" )
    server.sendall(transaction)
    buffer = server.recv(1024).decode()
    server.close()
    return buffer

def client_request_transfer(sndr="1", rcvr="2", amount="0"):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if sndr not in ['1','2','3'] : 
        return
    client_addr = clients[int(sndr)]
    client.connect(client_addr)
    transaction = str.encode("*".join([str("request_transfer"), str(sndr), str(rcvr), str(amount)])+"\n" )
    client.sendall(transaction)
    client.close()

def send_data(rcvr, data):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if rcvr == 'server':
        client_addr = server_addr
    else:
        client_addr = clients[int(rcvr) - 1]
    client.connect(client_addr)
    operation = str.encode(dumps(data))
    client.sendall(operation)
    client.close()
    

server_addr = ("127.0.0.1", 1234)
client1_addr = ("128.0.0.1", 1234)
client2_addr = ("128.0.0.2", 1234)
client3_addr = ("128.0.0.3", 1234)
clients = [client1_addr, client2_addr, client3_addr]

class Client:
    def __init__(self, id):
        self.time = 0
        self.queue = []
        self.id = id
        self.replies = 0
        self.client_addr = clients[id - 1]

    def receive_request_from_server(self, transaction):
        args = {
            'time': self.time,
            'sender': self.id,
            'transaction': transaction
        }
        self.add_to_queue(args)
        self.send_requests_to_clients(args)

    def receive_reply_from_client(self, args):
        self.replies += 1
        if self.replies == 2:
            self.execute()
    
    def receive_reply_from_client(self, args):
        if self.replies == 2:
            self.execute()

    def receive_release_form_client(self, args):
        self.queue.pop(0)
        self.execute()
    
    def execute(self):
        if self.queue[0][1] == self.id:
            self.replies = 0
            # send request to server to execute
            send_data('server', self.queue.pop(0))

    def send_requests_to_clients(self, args):
        for i, client in enumerate(clients):
            if i + 1 != self.id:
                self.time += 1
                data = {
                    'operation': 'request',
                    'sender': self.id,
                    'time': self.time,
                    'transaction': args['transaction']
                }
                send_data(str(i), data)
                
    
    def send_replies_to_clients(self):
        for i, client in enumerate(clients):
            if i + 1 != self.id:
                self.time += 1
                data = {
                    'operation': 'reply',
                    'sender': self.id,
                    'time': self.time
                }
                send_data(data, self.id, str(i))
    def add_to_queue(self, args):
        self.queue = sorted(self.queue.append((args['time'], args['sender'], args['transaction'])))

    def send_reply_to_client(self, args):
        self.add_to_queue(args)
        self.time = max(self.time, args['time']) + 1
        data = {
            'operation': 'reply',
            'sender': self.id,
            'time': self.time
        }
        send_data(args['sender'], data)

    def receive_reply_from_server(self):
        # send release to all clients
        self.queue.pop(0)
        for i, client in enumerate(clients):
            if i + 1 != self.id:
                self.time += self.time + 1
                data = {
                    'operation': 'release',
                    'sender': self.id,
                    'time': self.time
                }
                send_data(data, self.id, str(i))