from app import app
from app.forms import EditCardForm
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
    posts = []
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
        current_user.name_first = form.name_first.data
        current_user.name_last = form.name_last.data
        current_user.birthday = form.birthday.data
        current_user.gift_bday = form.gift_bday.data
        current_user.gift_xmas = form.gift_xmas.data
        current_user.update_profile(current_user.__dict__)
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.name_first.data = current_user.name_first
        form.name_last.data = current_user.name_last
        form.birthday.data = current_user.birthday
        form.gift_bday.data = current_user.gift_bday
        form.gift_xmas.data = current_user.gift_xmas
    return render_template('edit_profile.html', title='Edit Profile', form=form)


# Fix this base template inheritance first.
@app.route('/admin')
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html')


@app.route('/admin/cards/add_card', methods=['GET', 'POST'])
@login_required
def admin_add_card():
    form = AddNewCardForm()
    if form.validate_on_submit():
        new_card_dict = {
            'card_name': form.card_name.data,
            'description': form.description.data,
            'type': form.type.data,
            'released_on': form.released_on.data,
            'status': form.status.data,
            'quantity': form.quantity.data,
            'filename': form.filename.data
        }
        if not form.validate_card_name(new_card_dict):
            return redirect(request.url)
        if not form.validate_filename(new_card_dict):
            return redirect(request.url)
        Card.add_card(new_card_dict=new_card_dict)
        flash('Card added successfully.')
        return redirect('/admin/cards/add_card')
    elif request.method == 'GET':
        return render_template('admin_add_card.html', form=form)


# 'GET' or 'POST' or both?
@app.route('/admin/cards/<card_name>/delete_card', methods=['GET'])
@login_required
def admin_delete_card(card_name):
    card_name_dict = {'card_name': card_name}
    Card.delete_card(card_name_dict=card_name_dict)
    flash('Card deleted!')
    return redirect(url_for('admin_view_all_cards'))


@app.route('/admin/cards/all')
@login_required
def admin_view_all_cards():
    cards = Card.get_all_cards()
    return render_template('admin_view_cards.html', cards=cards)


@app.route('/admin/cards/<card_name>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_one_card(card_name):
    card_name_dict = {'card_name': card_name}
    card = Card.get_one_card(card_name_dict)
    form = EditCardForm(card.__dict__)
    if form.validate_on_submit():
        card_update_dict = {
            'original_card_name': form.original_card_name,
            'card_name': form.card_name.data,
            'description': form.description.data,
            'type': form.type.data,
            'released_on': form.released_on.data,
            'status': form.status.data,
            'quantity': form.quantity.data,
            'filename': form.filename.data
        }
        card.update_card(card_update_dict)
        flash('Your changes have been saved.')
        return redirect(url_for('admin_view_all_cards'))
    elif request.method == 'GET':
        form.card_name.data = card.card_name
        form.description.data = card.description
        form.type.data = card.type
        form.released_on.data = card.released_on
        form.status.data = card.status
        form.quantity.data = card.quantity
        form.filename.data = card.filename
    return render_template(
            'admin_edit_card_form.html',
            title='Edit a Card',
            form=form,
            card=card
            )

@app.route('/cards')
def view_cards():
    cards = Card.get_all_cards()
    return render_template('view_cards.html', cards=cards)