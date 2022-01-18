from flask import Flask, render_template, session, copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect
from threading import Lock
from util import *

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket_ = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
queue = []

@app.route('/')
def index():
    return render_template('index.html')

@socket_.on('my_event')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})

@socket_.on('queue_transfer')
def queue_transfer(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    txn = (message['data'][0],message['data'][1],message['data'][2])
    emit('my_response', {'data': f"Enqueued transfer of ${txn[2]} from {txn[0]} to {txn[1]}", 'count': session['receive_count']})
    queue.append(txn)
    
@socket_.on('execute_all_transfer')
def execute_all_transfer():
    session['receive_count'] = session.get('receive_count', 0) + 1
    if not queue:
        emit('my_response', {'data': f"No transfers to enqueue! Please enqueue a transfer request first.", 'count': session['receive_count']})
        return
    while queue:
        txn = queue.pop()
        sndr, rcvr, amt = txn[0],txn[1],txn[2]        
        emit('my_response', {'data': f"Now processing transfer of ${amt} from {sndr} to {rcvr}", 'count': session['receive_count']})
        #client_request_transfer(sndr,rcvr,amt)    
        sendMoney(sndr,rcvr,amt)    


@socket_.on('balance_inquiry')
def balance_inquiry(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    buffer = balanceInquire(message['data'])
    emit('my_response',
         {'data': f"{buffer} is the current balance of {message['data']}", 'count': session['receive_count']},
         broadcast=True)

@socket_.on('send_money_result')
def send_money_result(message):
    result, sndr, rcvr, amt = message['result'], message['data'][0],message['data'][1],message['data'][2]
    emit('my_response', {'data': f"Transfer of {amt} from {sndr} to {rcvr} was a {result}", 'count': '?'}, broadcast=True)


@socket_.on('disconnect_request')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()        

    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


if __name__ == '__main__':
    
    socket_.run(app, debug=True)