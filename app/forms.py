from app.models import User
from app.models import Card
from flask_wtf import FlaskForm
from flask import flash
from mysqlconnection import connectToMySQL
from wtforms import BooleanField
from wtforms import DateField
from wtforms import IntegerField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import Length
from wtforms.validators import ValidationError


db = __import__('config').Config.db


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()]) # Check against empty fields
    password = PasswordField('Password', validators=[DataRequired()]) # Check against empty fields
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Confirm password', validators=[DataRequired(), EqualTo('password')]
        )
    submit = SubmitField('Register')


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


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired()])
    about_me = TextAreaField('About me', validators=[
        Length(min=0, max=255)])
    submit = SubmitField('Submit')


    def __init__(self, original_username, new_about_me, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.new_about_me = new_about_me


    def validate_username(self, username):
        username_dict = {'username': username}
        if username.data != self.original_username:
            user = User.get_user_by_username(username_dict)
            if user is not None:
                raise ValidationError('Please use a different username.')


class AddNewCardForm(FlaskForm):
    name = StringField('Name', validators=[
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
        # 'ALTER TABLE' needed
    quantity = IntegerField('Quantity', validators=[
        DataRequired()])
    filename = StringField('Filename', validators=[
        DataRequired(),
        Length(min=0, max=127)])
    submit = SubmitField('Add card')


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


    def validate_card_edits(self, new_card_name, new_filename):
        card_edits_dict = {
            'new_card_name': new_card_name,
            'new_filename': new_filename
            }
        if new_card_name.data != self.original_card_name:
            card = Card.get_card_name_for_validation(card_edits_dict=card_edits_dict)
            if card is not None:
                raise ValidationError('Please use a different card name.')
        if new_filename.data != self.original_filename:
            card = Card.get_card_filename_for_validation(card_edits_dict=card_edits_dict)
            if card is not None:
                raise ValidationError('Please use a different filename.')