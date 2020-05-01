from datetime import datetime
from hashlib import md5
from flask_login import UserMixin
from app import db, login
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from time import time
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
import json
import os


# table for user likes or rates
rates = db.Table(
    'rates',
    db.Column('rater_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('rated_id', db.Integer, db.ForeignKey('user.id'))
)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    company = db.Column(db.String(120))
    phone = db.Column(db.String(30))
    password = db.Column(db.String(128), nullable=False)
    dateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    about = db.Column(db.String(2000))
    image = db.Column(db.String(30))
    rated = db.relationship(
        'User', secondary=rates,
        primaryjoin=(rates.c.rater_id == id),
        secondaryjoin=(rates.c.rated_id == id),
        backref=db.backref('rates', lazy='dynamic'), lazy='dynamic'
    )
    message_sent = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic')
    message_recieved = db.relationship('Message', foreign_keys='Message.recipient_id', backref='recipient', lazy='dynamic')

    last_message_read_time = db.Column(db.DateTime)

    notifications = db.relationship('Notification', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # generate password hash
    def set_password(self, password_hash):
        self.password = generate_password_hash(password_hash)

    # verify password hash
    def verify_password(self, password_hash):
        return check_password_hash(self.password, password_hash)


    # method for new message
    def new_message(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(Message.timestamp > last_read_time).count()

    # check if user is not rated
    # if not, then rate
    def rate(self, user):
        if not self.is_rate(user):
            self.rated.append(user)

    # check if user is rated
    # if true unrate user
    def unrate(self, user):
        if self.is_rate(user):
            self.rated.remove(user)

    # check for user if rated or not
    def is_rate(self, user):
        return self.rated.filter(
            rates.c.rated_id == user.id).count() > 0

    # setting avatar image
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
        
    
    # methods for reset passwords and generating tokens
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return None
        return User.query.get(id)

    # notification method 
    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# message class
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __ref__(self):
        return '<Massage {}>'.format(self.body)

# notification class
class Notification(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))