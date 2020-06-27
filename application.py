import os
from flask import Flask, session, render_template, url_for, request, redirect, flash
from sqlalchemy import create_engine
from flask_session import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from models import *
import requests
from werkzeug.security import check_password_hash, generate_password_hash





# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app = Flask(__name__)
#app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SESSION_TYPE'] = 'filesystem'
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://vbpmeocfxajymp:811a3bfe88d3942fc1e2131392fee3ebd1b2c037affe7cb74bce0a139cf0975f@ec2-34-194-198-176.compute-1.amazonaws.com:5432/d4g707hhuci1mn"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
bootstrap = Bootstrap(app)
db.init_app(app)
Session(app)

#login_manager = LoginManager()
#login_manager.init_app(app)
#login_manager.login_view = 'login'
# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
FLASK_DEBUG = 1


#set up users 


#@login_manager.user_loader
#def load_user(user_id):
    #return Users.query.get(int(user_id))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
	""" Log user in """ 
	session.clear()
	username = request.form.get('username')
	password = request.form.get('password')

	if not password:
		return render_template('index.html', password_error='Need password')
	elif not username:
		return render_template('index.html', user_error='Need username')	

	#user = Users.query.filter_by(username=request.form.get('username')).first()
	#if db.execute("SELECT * FROM registeredusers WHERE username = :username AND password = :password", {"username": username, "password": password}).rowcount == 0:
	#	return render_template('index.html', error='Invalid username or password')

	user = db.execute("SELECT * FROM registeredusers WHERE username = :username", 
		{"username": username}).fetchone()

	if user:
		if check_password_hash(user[4], password):
			session["user_id"] = user[0]
			session['user_name'] = user[3]
			return render_template('home.html')		
	#if user:
		#if check_password_hash(user.password, password):
		#	login_user(user)
		#	flash("Login Succesful")
		#	return render_template('home.html')

		return render_template('index.html', error='Invalid user or pass')
	
	
	
	return render_template("index.html")

@app.route('/search', methods=["GET"])
def search():	
	query = request.args.get('searchQuery')
	query = "%" + str(query) + "%" #checking for similarity 
	#check if query is empty OR not like any of the items 
	#set query to all lowercase 
	query = query.lower()
	#set values here to all lowercase...?
	#set a similarity# 	
	results = db.execute("SELECT * FROM books WHERE isbn LIKE :query OR lower(title) LIKE :query OR lower(author) LIKE :query OR year LIKE :query LIMIT 20", 
		{"query": query}).fetchall()
	if len(results) == 0:
		error_message = 'No search results'
		return render_template("home.html", error_message=error_message) 
	
	#books = results.fetchall()
	return render_template("results.html", results=results)


@app.route("/book/<int:book_id>", methods=["GET", "POST"])
def book(book_id):

	#book = db.execute("SELECT * FROM books WHERE id = :id",{"id": book_id}).fetchone()
	if request.method == "GET":
		book = db.execute("SELECT * FROM books WHERE id = :id",{"id": book_id}).fetchone()
		results = db.execute("SELECT registeredusers.username, reviews.review, reviews.rating FROM registeredusers JOIN reviews ON registeredusers.id = reviews.user_id WHERE book_id = :book_id",
			{"book_id":book_id}).fetchall()
		isbns = book[1]
		gd_reviews = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "woZVZTYzEs4vSfUBnsbp7A", "isbns": isbns})
		gd_reviews = gd_reviews.json()
		gd_review_book = gd_reviews['books'][0]
		
		return render_template('book.html', book=book, results=results, gd_review_book=gd_review_book)

	#else is for calling via the POST method
	else:

		user_id = session["user_id"]
		print(user_id)

		#check if user aready had submitted a review for this book 

		check_reviews = db.execute("SELECT * FROM reviews WHERE book_id = :book_id AND user_id = :user_id",{"book_id": book_id, "user_id": user_id})
		print(check_reviews)
		if check_reviews.rowcount == 1:
			flash("You have already left a review")
			return redirect('/book/' + str(book_id))


		review = request.form.get('review')
		rating = request.form.get('rating')

		#add the review if the user has not already submitted one!

		db.execute("INSERT INTO reviews (book_id, user_id, rating, review) VALUES (:book_id, :user_id, :rating, :review)", 
			{"book_id":book_id, "user_id":user_id, "review":review, "rating":rating})
		db.commit()
	
		
		return redirect('/book/' + str(book_id))


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
