"""
This module contains database models that store
the data for the application.
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
import json


class User(db.Model, UserMixin): # UserMixin helps with adding some methods to the db
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
    task_edit = db.Column(db.String(1000), nullable=True)
    options_edit = db.Column(db.String(300), nullable=True)

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
    due_date = db.Column(db.DateTime, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    mark_as_completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Task {}>".format(self.title)
    
    def _get_task_from_title(self, title):
        """This is to get the task id using the title"""
        task = Task.query.filter_by(title=title).first()
        if task is None:
            raise ValueError('No task with this name')
        return task

    def _get_task_from_id(self, id):
        """This is to get the task from the id"""
        task = Task.query.filter_by(id=id).first()
        if task is None:
            raise ValueError('No task with this name')
        return task

    def update_task(self, **kwargs):
        """This is to change th eattribute of the task in question"""
        for k, v in kwargs.items():
            if hasattr(Task, k):
                setattr(self, k, v)
            else:
                raise ValueError
        db.session.commit()
        return self


@login.user_loader
def load_user(id):
    return User.query.get(int(id))