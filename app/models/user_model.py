from flask_login import UserMixin
from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_token = db.Column(db.String, nullable=False)
    user_login = db.Column(db.String(50), nullable=False)
    user_password = db.Column(db.String(256), nullable=False)
    user_date = db.Column(db.String(16), nullable=False)