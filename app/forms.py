"""
This module contains objects that handles users registrations and signing in
"""


from flask_wtf import FlaskForm
from datetime import date
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    """
    This class represents the registration web form 
    It gets inputs from the user using wtforms fields.
    (StringField, PasswordField, SubmitField)
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """
        A function to help with easily validating username availability.
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username taken")
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("That email exists")
        
    


class LoginForm(FlaskForm):
    """
    This class represents the login web form
    It gets inputs from the user using wtforms fields.
    (StringField, PasswordField, SubmitField)
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class TasksForm(FlaskForm):
    task_title = StringField('Task TItle:', validators=[DataRequired(), Length(max=60)])
    description = TextAreaField('Description:', validators=[DataRequired()])
    due_date = DateField('Due Date:', validators=[DataRequired()], format='%Y-%m-%d')
    date_created = DateField('Date Created', validators=[DataRequired()], format='%Y-%m-%d', default=date.today())
    mark_as_completed = BooleanField('Mark as Completed')
    add_task = SubmitField('Add Task')