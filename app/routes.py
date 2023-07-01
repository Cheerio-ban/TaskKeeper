from flask import url_for, render_template, flash, redirect
from app.forms import RegistrationForm, LoginForm
from app import app


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("login requested for user {}, remember_me={}".format(
            form.username.data, form.remember_me.data
        ))
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign in', form=form)

@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Sign Up', form=form)