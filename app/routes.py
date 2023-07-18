from flask import url_for, render_template, flash, redirect, request
from app.forms import RegistrationForm, LoginForm, TasksForm
from app.models import User, Task
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    form = TasksForm()
    if form.validate_on_submit():
        task = Task(title=form.task_title.data, body=form.description.data)
        task.due_date = form.due_date.data
        task.author = current_user
        task.mark_as_completed = form.mark_as_completed.data
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('tasks'))
    tasks = Task.query.all()
    return render_template('home.html', tasks=tasks, form=form)

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
        next_page = request.args.get('next') # Handles urls stored in the next from login_required
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('User already exist, please login')
            return redirect(url_for('login'))
        new = User(username=form.username.data, email=form.email.data)
        new.set_password(form.password.data)
        db.session.add(new)
        db.session.commit()
        flash('congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form)

@app.route('/tasks')
@login_required
def tasks():
    form = TasksForm()
    tasks = Task.query.filter_by(author=current_user).all()
    return render_template('tasks.html', tasks=tasks, form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/contact')
def contact():
    return render_template('contact.html')