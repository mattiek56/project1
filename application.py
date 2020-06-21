import os

from flask import Flask, session, render_template, url_for, request, redirect, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from users import *

from werkzeug.security import check_password_hash, generate_password_hash





# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SESSION_TYPE'] = 'filesystem'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://vbpmeocfxajymp:811a3bfe88d3942fc1e2131392fee3ebd1b2c037affe7cb74bce0a139cf0975f@ec2-34-194-198-176.compute-1.amazonaws.com:5432/d4g707hhuci1mn"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
bootstrap = Bootstrap(app)
db.init_app(app)
Session(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# Set up database
#engine = create_engine(os.getenv("DATABASE_URL"))
#db = scoped_session(sessionmaker(bind=engine))
FLASK_DEBUG = 1


#set up users 


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
	""" Log user in """ 
	
	password = request.form.get('password')

	if not password:
		return render_template('index.html', password_error='Need password')
	elif not request.form.get('username'):
		return render_template('index.html', user_error='Need username')	

	user = Users.query.filter_by(username=request.form.get('username')).first()
	if user:
		if check_password_hash(user.password, password):
			login_user(user)
			flash("Login Succesful")
			return render_template('home.html')

		return render_template('index.html', error='invalid user or pass')
	#if db.execute("SELECT * FROM registeredusers WHERE username = :username AND password = :password", {"username": username, "password": password}).rowcount == 0:
		#return render_template('index.html', error='Invalid username or password')
	
	
	return render_template("index.html")

@app.route("/register")
def register():
	return render_template("register.html", register=True)


@app.route("/register/success", methods=["POST", "GET"])
def success():
	
	#add in a check to see if username is unique!!! 

	#hash the user password to be stored in the DB
	hashedPassword = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

	new_user = Users(firstname = request.form.get('FirstName'), lastname = request.form.get('LastName'), email = request.form.get('Email'), 
		password = hashedPassword, username = request.form.get('username'))
	#db.execute("INSERT INTO registeredusers (firstName, lastName, username, password) VALUES (:firstName, :lastName, :username, :password)",{"firstName": firstName, "lastName": lastName, "username": username, "password": password})
	db.session.add(new_user)
	db.session.commit()
	
	

	return render_template("home.html")	

@app.route('/sign_out')
def sign_out():
    #logout user form system

    logout_user()
    return redirect(url_for('index'))	
