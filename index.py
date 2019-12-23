from datetime import date
from flask import Flask, redirect, request, url_for, render_template, session
import sqlite3 
app = Flask(__name__, static_folder='static')       # our Flask app
app.secret_key = "super secret key"
DB_FILE = 'mydb.db'    		# file for our Database
connection = sqlite3.connect(DB_FILE, check_same_thread=False)
import sys
@app.route('/')
def index():
	
	return render_template('index.html')

@app.route('/guestbook', methods=['POST', 'GET'])
def guestbook():
	"""
	Accepts POST requests, and processes the form;
	Redirect to view when completed.
	"""
	connection = sqlite3.connect(DB_FILE)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM guestbook")
	rv = cursor.fetchall()
	cursor.close()
	return render_template("guestbook.html",entries=rv)
    


def _insert(name, email, comment):
	"""
	put a new entry in the database
	"""
	params = {'name':name, 'email':email, 'comment':comment}
	connection = sqlite3.connect(DB_FILE)
	cursor = connection.cursor()  
	cursor.execute("insert into guestbook VALUES (:name, :email, :comment)",params)
	connection.commit()
	cursor.close()

@app.route('/sign', methods=['POST'])
def sign():
	"""
	Accepts POST requests, and processes the form;
	Redirect to index when completed.
	"""
	_insert(request.form['name'], request.form['email'], request.form['comment'])
	return redirect(url_for('guestbook'))

@app.route('/d2', methods=['POST', 'GET'])
def reviews():
	"""
	Accepts POST requests, and processes the form;
	Redirect to view when completed.
	"""
	connection = sqlite3.connect(DB_FILE)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM reviews")
	rv = cursor.fetchall()
	cursor.close()
	return render_template("d2.html",entries=rv)

def _insert1(username, comment):
	"""
	put a new entry in the database
	"""
	params = {'username':username, 'comment':comment}
	connection = sqlite3.connect(DB_FILE)
	cursor = connection.cursor()  
	cursor.execute("insert into reviews VALUES (:username, :comment)",params)
	connection.commit()
	cursor.close()

@app.route('/sign1', methods=['POST'])
def sign1():
	"""
	Accepts POST requests, and processes the form;
	Redirect to index when completed.
	"""
	_insert1(session['username'], request.form['comment'])
	return redirect(url_for('reviews'))


@app.route('/uncharted', methods=['POST', 'GET'])
def reviews1():
	"""
	Accepts POST requests, and processes the form;
	Redirect to view when completed.
	"""
	connection = sqlite3.connect(DB_FILE)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM reviews1")
	rv = cursor.fetchall()
	cursor.close()
	return render_template("uncharted.html",entries=rv)

def _insert2(username, comment):
	"""
	put a new entry in the database
	"""
	params = {'username':username, 'comment':comment}
	connection = sqlite3.connect(DB_FILE)
	cursor = connection.cursor()  
	cursor.execute("insert into reviews1 VALUES (:username, :comment)",params)
	connection.commit()
	cursor.close()

@app.route('/sign2', methods=['POST'])
def sign2():
	"""
	Accepts POST requests, and processes the form;
	Redirect to index when completed.
	"""
	_insert2(session['username'], request.form['comment'])
	return redirect(url_for('reviews1'))


@app.route('/hz', methods=['POST', 'GET'])
def reviews2():
	"""
	Accepts POST requests, and processes the form;
	Redirect to view when completed.
	"""
	connection = sqlite3.connect(DB_FILE)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM reviews2")
	rv = cursor.fetchall()
	cursor.close()
	return render_template("hz.html",entries=rv)

def _insert3(username, comment):
	"""
	put a new entry in the database
	"""
	params = {'username':username, 'comment':comment}
	connection = sqlite3.connect(DB_FILE)
	cursor = connection.cursor()  
	cursor.execute("insert into reviews2 VALUES (:username, :comment)",params)
	connection.commit()
	cursor.close()

@app.route('/sign3', methods=['POST'])
def sign3():
	"""
	Accepts POST requests, and processes the form;
	Redirect to index when completed.
	"""
	_insert3(session['username'], request.form['comment'])
	return redirect(url_for('reviews2'))

#SIGN IN.

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        query = "select * from accounts where username = '" + request.form['username']
        query = query + "' and password = '" + request.form['password'] + "';"
        cur = connection.execute(query)
        rv = cur.fetchall()
        
        cur.close()
        if len(rv) == 1:
            session['username'] = request.form['username']
            
            session['logged in'] = True

            return redirect('/')
        else:
            return render_template('login.html', msg="Check your login details and try again.")
    else:
        return render_template('login.html')

#LOG OUT

@app.route('/logout')
def logout():
	session.pop('logged in', None)
	session.pop('username', None)
	return redirect('/')

	#SIGN UP.
def _insertuser(username, password):
    params = {'username': username, 'password': password}
    cursor = connection.cursor()
    cursor.execute("insert into accounts(username, password) values (:username, :password)"
                   , params)
    connection.commit()
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        _insertuser(request.form['user'], request.form['pass'])
        return render_template('signup.html', msg="Thank you for signing up!")
    else:
        return render_template('signup.html')

if __name__ == '__main__':			
	app.run(debug=True)