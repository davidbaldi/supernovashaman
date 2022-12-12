from app import app
from app.forms import EditProfileForm
from app.forms import LoginForm
from app.forms import AddNewCardForm
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
    user_query_dict = {'username': username}
    user = User.get_user_by_username(user_query_dict)
    if user is not None:
        return render_template('user.html', user=user)
    return render_template('404.html')


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.about_me)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.update_profile(current_user.__dict__)
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


# Temporary
@app.route('/cards')
@login_required
def display_all_cards():
    return render_template('_card_raw.html', card=None)


@app.route('/admin/cards/add_card', methods=['GET', 'POST'])
@login_required
def add_card():
    form = AddNewCardForm()
    if form.validate_on_submit():
        new_card_dict = {
            'name': form.name.data,
            'description': form.description.data,
            'type': form.type.data,
            'released_on': form.released_on.data,
            'status': form.status.data,
            'quantity': form.quantity.data,
            'filename': form.filename.data
        }
        Card.add_card(new_card_dict=new_card_dict)
        return redirect('/admin/add_card')
    return render_template('admin_add_card.html', form=form)


@app.route('/admin/cards/view_all_cards')
@login_required
def view_all_cards():
    cards = Card.get_all_cards()
    return render_template('admin_view_all_cards.html', cards=cards)