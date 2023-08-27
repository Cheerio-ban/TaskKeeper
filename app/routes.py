from flask import url_for, render_template, flash, redirect, request
from app.forms import RegistrationForm, LoginForm, TasksForm, EditFindTask, EditTaskForm
from app.models import User, Task
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db


@app.route('/<username>', methods=['GET', 'POST'])
@login_required
def home(username):
    if username != current_user.username:
        return redirect(url_for('login'))
    form = TasksForm()
    if form.validate_on_submit():
        task = Task(title=form.task_title.data, body=form.description.data)
        task.due_date = form.due_date.data
        task.author = current_user
        task.mark_as_completed = form.mark_as_completed.data
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('tasks', username=current_user.username))
    tasks = Task.query.all()
    return render_template('home.html', tasks=tasks, form=form)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Checks if user is logged in and returns user to home if they are.
        return redirect(url_for('home', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()  
        if user is None or not user.check_password(form.password.data):
            # If user doesn't get validated.
            flash('Invalid username or Password', 'error')
            return redirect(url_for('login'))
        # if user gets validated
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next') # Handles urls stored in the next from login_required
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home', username=current_user.username)
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
            flash('User already exist, please login', 'error')
            return redirect(url_for('login'))
        new = User(username=form.username.data, email=form.email.data)
        new.set_password(form.password.data)
        db.session.add(new)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form)


@app.route('/<username>/tasks/edit_task', methods=['GET', 'POST'])
@login_required
def edit_task(username):
    form = EditFindTask()
    tasks = Task.query.filter_by(author=current_user).all()
    if username != current_user.username:
        return redirect(url_for('login'))
    if form.validate_on_submit():
        if form.identifier.data == "one":
            task = Task.query.filter_by(id=int(form.value.data)).first()
            if task is None:
                flash(f'No task with the ID "{form.value.data}"')
                return redirect(url_for('tasks', username=current_user.username))
        else:
            task = Task.query.filter_by(title=form.value.data).first()
            if task is None:
                flash(f'No task with the title "{form.value.data}"')
                return redirect(url_for('home', username=current_user.username))
        if task.author.username != current_user.username:
            flash(f'No task with the ID "{form.value.data}"')
            return redirect(url_for('tasks', username=current_user.username))
        current_user.task_edit = str(task.id)
        db.session.commit()
        return redirect(url_for('edit_task_id', username=current_user.username, id=task.id))
    return render_template('edit_task.html', tasks=tasks, form=form)


@app.route('/<username>/tasks/edit_task/task', methods=['GET', 'POST'])
@login_required
def edit_task_id(username):
    if username != current_user.username:
        redirect(url_for('login'))
    form = EditTaskForm()
    id = int(request.args.get('id'))
    if str(id) != current_user.task_edit:
        redirect(url_for('edit_task', username=current_user.username))
    task = Task.query.filter_by(id=id).first()
    if form.validate_on_submit():
        update = {}
        update['title'] = form.task_title.data
        update['body'] = form.description.data
        update["due_date"] = form.due_date.data
        update['mark_as_completed'] = form.mark_as_completed.data
        task.update_task(**update)
        return redirect(url_for('tasks', username=username))
    tasks = Task.query.filter_by(id=id)
    return render_template('edit_task.html', task=task, tasks=tasks, form_edit=form)


@app.route('/<username>/tasks')
@login_required
def tasks(username):
    form = TasksForm()
    if username != current_user.username:
        return redirect(url_for('login'))
    tasks = Task.query.filter_by(author=current_user).all()
    return render_template('tasks.html', tasks=tasks, form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/contact')
def contact():
    return render_template('contact.html')