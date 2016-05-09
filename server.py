from flask import Flask, url_for, render_template, flash, redirect, request, session
from mysqlconnection import MySQLConnector 
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

app = Flask(__name__)
app.secret_key = 'IamSecret'
mysql = MySQLConnector(app, 'email_val_db')

@app.route('/', methods=['GET', 'POST'])
def index():	
	# start mySQL select
	friends_data_query = "SELECT * FROM users"
	friends_list = mysql.query_db(friends_data_query)
	#end mysql select
	return render_template('index.html', friends_data = friends_list)

@app.route('/friends', methods=['POST'])
def create():


	if (len(request.form['email']) <1 ):
		flash('Please enter your email')
		
	elif not EMAIL_REGEX.match(request.form['email']):
		flash('please enter a valid email')
		
	else:
		# start mySQL insert
		query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (:firstname, :lastname, :email, NOW(), NOW() )"
		data = {
				'firstname': request.form['first_name'],
				'lastname': request.form['last_name'],
				'email': request.form['email']
			}
		mysql.query_db(query, data)
		#end mysql select

		return redirect('/')
	#add friends
	return redirect('/')

@app.route('/friends/<id>/edit', methods=['GET'])
def edit(id):
	#write a query to select a specific user by id at every point where we want to insert data
	query = "SELECT * FROM users WHERE id = :id"

	data = {
		'id' : id
	}

	friend = mysql.query_db(query, data)

	return render_template('success.html', edit_friend = friend[0])

@app.route('/friends/<id>',  methods=['POST'])
def update(id):
	query = "UPDATE users SET first_name = :first_name, last_name = :last_name, email = :email WHERE id = :id"

	data = {
	       'first_name': request.form['first_name'], 
	       'last_name':  request.form['last_name'],
	       'email': request.form['email'],
	       'id': id
	}
	mysql.query_db(query, data)

	return redirect('/')

@app.route('/friends/<id>/delete',  methods=['GET','POST'])
def destroy(id):

	query = "DELETE FROM users WHERE id = :id"
	data = {'id': id }
	mysql.query_db(query, data)

	return redirect('/')

app.run(debug=True)