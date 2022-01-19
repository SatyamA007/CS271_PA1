from mimetypes import init
from client import *

# if __name__=="__main__":    
    
#     userIO = "1"
#     while True:
#         userIO = input("Enter transaction type(1-BalanceInquiry, 2-SendMoney, 0-Exit):")
#         if userIO=="1":
#             buffer = balanceInquire()
#             print(f"Your balance is = {buffer}")
#         elif userIO=="2":
#             receiver = input("Enter receiver:" )
#             amount = input("Enter amount to send:")
#             buffer = sendMoney("me", receiver, amount)
#             print(f"Transfer of {amount} to {receiver} was {buffer}")
        
if __name__=="__main__":
    client_object = Client("1")
    ip, port = client_object.client_addr
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip,port))
    server.listen(10)
    
    while True:
        client,address = server.accept()
        
        print(f"Connection Established - {address[0]}, {address[1]}")
        message = client.recv(1024)
        
        args = loads(message)
        print(args)

        if args['sender'] == "server_request":
            ## add to queue and send to all other clients
            # transaction, sender, receiver, amount - in args
            client_object.receive_request_from_server(args['transaction'])
        elif args['sender'] == "server_reply":
            client_object.receive_reply_from_server(args)
        else:
            ## operation: request. Add to queue and send reply
            if args['operation'] == 'request':
                client_object.send_reply_to_client(args)

            ## operation: reply. If all replies, check if at head of queue and execute
            elif args['operation'] == 'reply':
                client_object.receive_reply_from_client(args)

            ## operation: release. If all replies, check if at head of queue and execute
            elif args['operation'] == 'release':
                client_object.receive_release_form_client(args)



    


    
