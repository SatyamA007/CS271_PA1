from mimetypes import init
import socket

def balanceInquire():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((ip,port))    
    transaction = str.encode("*".join([str("balance"), str("me"), str("receiver"), str("100")]) +"\n")
    server.sendall(transaction)
    buffer = server.recv(1024).decode()
    server.close()
    return buffer

def sendMoney(sndr="me", rcvr="receiver", amount="0"):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((ip,port))
    transaction = str.encode("*".join([str("sendMoney"), str(sndr), str(rcvr), str(amount)])+"\n" )
    server.sendall(transaction)
    buffer = server.recv(1024).decode()
    server.close()
    return buffer
    
ip = "127.0.0.1"
port = 1234

if __name__=="__main__":    
    
    userIO = "1"
    while(userIO!="0"):
        userIO = input("Enter transaction type(1-BalanceInquiry, 2-SendMoney, 0-Exit):")
        if userIO=="1":
            buffer = balanceInquire()
            print(f"Your balance is = {buffer}")
        elif userIO=="2":
            receiver = input("Enter receiver:" )
            amount = input("Enter amount to send:")
            buffer = sendMoney("me", receiver, amount)
            print(f"Transfer of {amount} to {receiver} was {buffer}")
        

    


    
