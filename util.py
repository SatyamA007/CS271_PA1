
import socket

def balanceInquire():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(server_addr)    
    transaction = str.encode("*".join([str("balance"), str("me"), str("receiver"), str("100")]) +"\n")
    server.sendall(transaction)
    buffer = server.recv(1024).decode()
    server.close()
    return buffer

def sendMoney(sndr="me", rcvr="receiver", amount="0"):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(server_addr)
    transaction = str.encode("*".join([str("sendMoney"), str(sndr), str(rcvr), str(amount)])+"\n" )
    server.sendall(transaction)
    buffer = server.recv(1024).decode()
    server.close()
    return buffer
    
server_addr = ("127.0.0.1", 1234)
client1_addr = ("128.0.0.1", 1234)
client2_addr = ("128.0.0.2", 1234)
client3_addr = ("128.0.0.3", 1234)
