from flask import Flask, render_template, session, copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect
from threading import Lock
from util import *
import os 
import subprocess

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket_ = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


@app.route('/')
def index():
    return render_template('index.html')


@socket_.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})

@socket_.on('send_money', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    sndr,rcvr,amt = message['data'][0],message['data'][1],message['data'][2]
    buffer =  "pass" if (int(balanceInquire(sndr)) - int(amt)>0) else "fail"
    emit('my_response',
         {'data': f"Transfer of ${amt} from {sndr} to {rcvr} was {buffer}", 'count': session['receive_count']})
    client_request_transfer(sndr,rcvr,amt)    



@socket_.on('balance_inquiry', namespace='/test')
def balance_inquiry(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    buffer = balanceInquire(message['data'])
    emit('my_response',
         {'data': f"{buffer} is the current balance of {message['data']}", 'count': session['receive_count']},
         broadcast=True)


@socket_.on('disconnect_request', namespace='/test')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


if __name__ == '__main__':
    os.startfile('python', 'tcpServer.py')
    subprocess.call('start /wait python tcpServer.py', shell=True)

    socket_.run(app, debug=True)