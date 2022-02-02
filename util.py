
from http import server
import socket
from collections import deque
from pickle import dumps, loads

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
max_tcp_connections = 15

server_addr = ("127.0.0.1", 1234)
client1_addr = ("127.0.0.1", 4435)
client2_addr = ("127.0.0.1", 7736)
client3_addr = ("127.0.0.1", 9937)
clients = [client1_addr, client2_addr, client3_addr]

