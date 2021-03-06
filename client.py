from util import *
# import logging
import threading
import time

# format = "%(asctime)s: %(message)s"
# logging.basicConfig(format=format, level=print,
#                     datefmt="%H:%M:%S")

class Client:
    def __init__(self, id):
        print('Initializing client ', id)
        self.time = 0
        self.queue = []
        self.id = id
        self.replies = 0
        self.client_addr = clients[int(id) - 1]

    def receive_request_from_server(self, transaction):
        print('Received request from server. Transaction: ', str(transaction))
        self.time += 1
        args = {
            'time': self.time,
            'sender': self.id,
            'transaction': transaction
        }
        self.add_to_queue(args)
        self.send_requests_to_clients(args)

    def receive_reply_from_client(self, args):
        print('Received reply from ', args['sender'])
        self.replies += 1
        if self.replies >= 2:
            self.execute()
    
    def receive_release_form_client(self, args):
        print('Release received from .............', args['sender'])
        if self.queue and args['sender'] != self.id:
            self.queue.pop(0)
        self.execute()
    
    def thread_function_execute(self):
        print('Head of execution queue: ', list([x[0:2] for x in self.queue]))
        print("Execution thread starting")
        time.sleep(3)
        
        if self.replies >= 2 and self.queue and self.queue[0][1] == self.id:
            print('Executing transfer request')
            self.replies -= 2
            # send request to server to execute
            data = self.queue.pop(0)
            args = {
                'transaction': data[2],
                'from': self.id
            }
            send_data('server', args)
        print("Execution thread finishing", list([x[0:2] for x in self.queue]))
        
    def execute(self):
        print("Main    : before creating thread")
        x = threading.Thread(target=self.thread_function_execute, args=())
        print("Main    : before running thread")
        x.start()
        print("Main    : all done")

    def thread_function_send_requests(self, args):
        time.sleep(3)
        print('Sending requests to clients....')
        for i, client in enumerate(clients):
            if i + 1 != int(self.id):
                data = {
                    'operation': 'request',
                    'sender': self.id,
                    'time': args['time'],
                    'transaction': args['transaction']
                }
                send_data(str(i + 1), data)
    def send_requests_to_clients(self, args):
        print("Broadcast    : before creating thread")
        x = threading.Thread(target=self.thread_function_send_requests, args=(args,))
        print("Broadcast    : before running thread")
        x.start()
        print("Broadcast    : all done")
                
    def add_to_queue(self, args):
        self.queue.append([args['time'], args['sender'], args['transaction']])
        self.queue.sort(key= lambda x: (x[0], int(x[1])))
        print('Adding new request',  list([x[0:2] for x in self.queue]))

    def send_reply_to_client(self, args):
        print('Sending reply to client', args['sender'])
        self.time = max(self.time, args['time']) + 1
        self.add_to_queue(args)
        
        data = {
            'operation': 'reply',
            'sender': self.id,
            'time': self.time
        }
        send_data(args['sender'], data)

    def receive_reply_from_server(self, args):
        print('Finished execution. Reply from server: ', args['result'])
        # send release to all clients
        self.time += 1
        for i, client in enumerate(clients):
            data = {
                'operation': 'release',
                'sender': self.id,
                'time': self.time
            }
            send_data(str(i + 1), data)