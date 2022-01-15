
import socket

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

    
server_addr = ("127.0.0.1", 1234)
client1_addr = ("128.0.0.1", 1234)
client2_addr = ("128.0.0.2", 1234)
client3_addr = ("128.0.0.3", 1234)
clients = [client1_addr, client2_addr, client3_addr]