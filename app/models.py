"""
This module contains database models that store
the data for the application.
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    """
    A class representing a user in the database using SQLAlchemy
    objects.
    It uses a one-to-many relationship with the task object below via 
    the posts attribute.
    It gives the task object a pseudo attribute via the backref argument.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Task', backref='author', lazy='dynamic')

    def __repr__(self):
        return "<User {}>".format(self.username)
    
    def set_password(self, password):
        """ Sets the password_hash as a hash of the password provided. """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """ Compares password gotten with the password in the database """
        return check_password_hash(self.password_hash, password)

    

class Task(db.Model):
    """
    A class representing a task in the database using SQLAlchemy
    objects.
    It has a many-to-one relationship with the User object above
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Task {}>".format(self.title)