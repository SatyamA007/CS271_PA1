from mimetypes import init
from util import *


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
        

    


    
