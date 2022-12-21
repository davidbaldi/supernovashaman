from app.models import User
from app.models import Card
from flask_wtf import FlaskForm
from flask import flash
from mysqlconnection import connectToMySQL
from wtforms import BooleanField
from wtforms import DateField
from wtforms import IntegerField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import InputRequired
from wtforms.validators import Length
from wtforms.validators import NumberRange
from wtforms.validators import ValidationError


db = __import__('config').Config.db


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Let\'s go!')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        # 'Confirm password', validators=[DataRequired(), EqualTo('password')]
        'Confirm password', validators=[DataRequired()]
        )
    submit = SubmitField('Sign me up!')


    def does_email_exist(self, new_user_dict):
        query = """
            SELECT * FROM users
            WHERE email = %(email)s;
            """
        if connectToMySQL(db).query_db(query, new_user_dict):
            return True


    def does_username_exist(self, new_user_dict):
        query = """
            SELECT * FROM users
            WHERE username = %(username)s;
            """
        if connectToMySQL(db).query_db(query, new_user_dict):
            return True


    def do_passwords_match(self, password, password2):
        if password != password2:
            return False
        return True


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired()])
    about_me = TextAreaField('About me', validators=[
        Length(min=0, max=255)])
    name_first = StringField('First name', validators=[
        Length(min=0, max=63)])
    name_last = StringField('Last name', validators=[
        Length(min=0, max=63)])
    birthday = DateField('Birthday')
    gift_bday = BooleanField('Send me a birthday gift next year!')
    gift_xmas = BooleanField('Send me a Christmas gift next year!')
    submit = SubmitField('Submit')


    def __init__(self, original_username, new_about_me):
        super(EditProfileForm, self).__init__()
        self.original_username = original_username
        self.new_about_me = new_about_me


class AddNewCardForm(FlaskForm):
    card_name = StringField('Name', validators=[
        DataRequired()])
    description = TextAreaField('Description', validators=[
        DataRequired(),
        Length(min=0, max=1023)])
    type = SelectField('Type', validators=[
        DataRequired()],
        choices=['Entity', 'Item', 'Helper', 'Philosophy', 'Spirit'])
    released_on = DateField('Release Date', validators=[
        DataRequired()])
    status = SelectField('Status', validators=[
        DataRequired()],
        choices=['in stock', 'Limited edition!', 'Private collection'])
    quantity = IntegerField('Quantity', validators=[
        InputRequired(),
        NumberRange(min=0)])
    filename = StringField('Filename', validators=[
        DataRequired(),
        Length(min=0, max=127)])
    submit = SubmitField('Add card')


    def validate_card_name(self, card_edits_dict):
        if Card.does_card_name_exist(card_edits_dict):
            flash('Card name already exists.')
            return False
        return True


    def validate_filename(self, card_edits_dict):
        if Card.does_filename_exist(card_edits_dict):
            flash('Filename already exists.')
            return False
        return True


class EditCardForm(FlaskForm):
    card_name = StringField('Card Name', validators=[
        DataRequired()])
    description = TextAreaField('Description', validators=[
        DataRequired(),
        Length(min=0, max=1023)])
    type = StringField('Type', validators=[
        DataRequired(),
        Length(min=0, max=15)])
    released_on = DateField('Release Date', validators=[
        DataRequired()])
    status = StringField('Status', validators=[
        DataRequired(),
        Length(min=0, max=32)])
    quantity = IntegerField('Quantity', validators=[
        DataRequired()])
    filename = StringField('Filename', validators=[
        DataRequired(),
        Length(min=0, max=127)])
    submit = SubmitField('Submit Changes')


    def __init__(self, card_stats, *args, **kwargs):
        super(EditCardForm, self).__init__(*args, **kwargs)
        self.original_card_name = card_stats['card_name']
        self.original_filename = card_stats['filename']


    def validate_card_name(self, card_edits_dict):
        if Card.does_card_name_exist(card_edits_dict):
            flash('Card name already exists.')
            return False
        return True

    
    def validate_filename(self, card_edits_dict):
        if Card.does_filename_exist(card_edits_dict):
            flash('Filename already exists.')
            return False
        return True