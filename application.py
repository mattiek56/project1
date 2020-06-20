import os

from flask import Flask, session, render_template, url_for, request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


#login_manager = LoginManager()
#login_manager.init_app(app)
#login_manager.login_view = 'login'




# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
FLASK_DEBUG = 1

#@login_manager.user_loader
#def load_user(user_id):
 #   return User.query.get(int(user_id))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home", methods=["POST", "GET"])
def login():
	
	username = request.form.get('username')
	password = request.form.get('password')
	if db.execute("SELECT * FROM registeredusers WHERE username = :username AND password = :password", {"username": username, "password": password}).rowcount == 0:
		return render_template('index.html', error='Invalid username or password')
	
	
	return render_template("home.html")

@app.route("/register")
def register():
	return render_template("register.html", register=True)


@app.route("/register/success", methods=["POST", "GET"])
def success():
	firstName = request.form.get('FirstName')	
	lastName = request.form.get('LastName')	
	password = request.form.get('password')
	username = request.form.get('username')
	db.execute("INSERT INTO registeredusers (firstName, lastName, username, password) VALUES (:firstName, :lastName, :username, :password)",{"firstName": firstName, "lastName": lastName, "username": username, "password": password})
	db.commit()
	users = db.execute("SELECT * FROM registeredusers").fetchall()
	

	return render_template("home.html", firstName=firstName)	

@app.route('/sign_out')
def sign_out():
    #session.pop('username')
    return redirect(url_for('index'))	
