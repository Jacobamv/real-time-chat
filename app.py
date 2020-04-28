from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO, send
from models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Jacob ahuenniy proger'
socketio = SocketIO(app)

@app.route('/')
def index():
	if session.get("user") is None:
		return redirect('/login')
	else:
		messages = Messages.select()
		return render_template('index.html', messages=messages, user=session.get('user'))

@app.route('/login')
def showLogin():
	return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def savelog():
	username = request.form['name']
	session['user'] = username
	return redirect('/', code=302)



@socketio.on('message')
def handleMessage(msg):
	print('Message' + msg)
	ms = Messages(message = msg, From = session.get('user'))
	ms.save()
	msg = str(session.get('user')) + ' : ' + str(msg)
	send(msg, broadcast = True)


if __name__ == '__main__':
	socketio.run(app, debug = True)