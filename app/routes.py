from app import app
from app.forms import EditProfileForm
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.models import User
from app.models import Card
from datetime import datetime
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.urls import url_parse


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        current_user.record_last_seen(current_user.__dict__)


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'David B.'},
            'body': 'Beautiful day in Portage Park!'
        },
        {
            'author': {'username': 'David W.'},
            'body': 'Beautiful day in Buena Park!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit(): # Returns 'False' if 'GET' request
        user_dict = {
            'username': form.username.data,
            'password': form.password.data,
            }
        user = User.get_user_by_username(user_dict)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        session['id'] = user.id
        session['username'] = user.username
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect('index')
    return render_template('login.html', title='Sign in', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user_dict = {
            'username': form.username.data,
            'email': form.email.data,
            'password': form.password.data
            }
        if form.does_email_exist(new_user_dict):
            flash('Please use a different email.')
            return render_template('register.html', title='Register', form=form)
        if form.does_username_exist(new_user_dict):
            flash('Please use a different username.')
            return render_template('register.html', title='Register', form=form)
        User.add_user(new_user_dict)
        user = User.get_user_by_username(new_user_dict)
        user.set_password(new_user_dict)
        flash(f'Welcome to my site, {form.username.data}!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    # How to rewrite without using 'username'?
    return render_template('user.html', user=current_user)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.about_me)
    if form.validate_on_submit():
        current_user.update_
        (current_user.__dict__)
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)