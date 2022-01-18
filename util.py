
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
    operation = dumps(data)
    client.sendall(operation)
    client.close()
    

server_addr = ("127.0.0.1", 1234)
client1_addr = ("127.0.0.1", 1235)
client2_addr = ("127.0.0.1", 1236)
client3_addr = ("127.0.0.1", 1237)
clients = [client1_addr, client2_addr, client3_addr]

