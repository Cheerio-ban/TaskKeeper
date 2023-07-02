from flask import url_for, render_template, flash, redirect
from app.forms import RegistrationForm, LoginForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from app import app


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Checks if user is logged in and returns user to home if they are.
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()  
        if user is None or not user.check_password(form.password.data):
            # If user doesn't get validated.
            flash('Invalid username or Password')
            return redirect(url_for('login'))
        # if user gets validated
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign in', form=form)

@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Sign Up', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))