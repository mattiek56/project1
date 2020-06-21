from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

db = SQLAlchemy()

class Users(UserMixin, db.Model):
    __tablename__ = "registeredusers"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.Integer, nullable=False)


