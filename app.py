from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO, send
from models import *
from peewee import *
import sqlite3
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key '
socketio = SocketIO(app)

@app.route('/')
def index():
	if session.get("user") is None:
		return redirect('/login')


	name = session.get('user')
	m = Messages.select(Messages.From, Messages.room).distinct().where(Messages.to == name)
	return render_template('index.html', name=name, rows=m)






@app.route('/', methods=['GET', 'POST'])
def Gotoroom():
	_name = request.form['user']
	session['userr'] = _name
	us = Users.get(Users.name==_name)
	arr = [_name ,session.get('user')]
	arr.sort()
	return redirect('/'+arr[0]+'|'+arr[1],code=302)




@app.route('/<roomname>')
def Showroom(roomname):
	if session.get("user") is None:
		return redirect('/login')
	session['roomname'] = roomname
	conn = sqlite3.connect('db.db')
	c2 = conn.cursor()
	c2.execute('''SELECT * FROM messages WHERE room = ?;''', (roomname,))
	rows = c2.fetchall()
	return render_template('chat.html', messages=rows, user=session.get('user'), wth=session.get('userr'))



@app.route('/login')
def showLogin():
	return render_template('login.html')





@app.route('/login/sign-up', methods=['GET', 'POST'])
def signUp():
	_name = request.form['username']
	_pass = request.form['password']
	us = Users(name=_name, password=_pass)
	us.save()
	return redirect('/', code=302	)






@app.route('/login/sign-in', methods=['GET', 'POST'])
def signIn():
	_name = request.form['username']
	_pass = request.form['password']
	us = Users.get(Users.name==_name)
	if _pass == us.password:
		session['user'] = _name
		return redirect('/', code=302)
	else:
		return "Password was wrooooong"






@socketio.on('message')
def handleMessage(msg):
	r = session.get('roomname')
	r = str(r).split('|')
	if r[0] == session.get('user'):
		to = r[1]
	else:
		to = r[0]
	ms = Messages(message = msg, From = session.get('user'), to = to, room = session.get('roomname'))
	ms.save()
	#msg = '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">'+ msg +'</div><div class="img_cont_msg"><img class="rounded-circle user_img_msg"></div></div>'
	send(msg, broadcast = True)



if __name__ == '__main__':
	socketio.run(app, debug = True)