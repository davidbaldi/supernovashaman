from app import login
from flask_login import UserMixin
from flask import session
from hashlib import md5
from mysqlconnection import connectToMySQL
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

db = __import__('config').Config.db


@login.user_loader
def load_user(id):
    return User.get_user_by_id(id)


class User(UserMixin):

    def __init__(self, user_dict):
        self.id = user_dict['id']
        self.email = user_dict['email']
        self.username = user_dict['username']
        self.password_hash = user_dict['password_hash']
        self.name_first = None
        self.name_last = None
        self.about_me = user_dict['about_me']
        self.registered_on = None
        self.admin_privilege = None
        self.birthday = None
        self.wants_birthday_gift = None
        self.wants_christmas_gift = None
        self.invite_code: None
        self.favorite_cards = []
        self.address = {}
        self.cart = {}
        self.orders = {}


    @classmethod
    def add_user(cls, new_user_dict):
        query = """
                INSERT INTO users (
                    username,
                    email
                    )
                VALUES (
                    %(username)s,
                    %(email)s
                    );
                """
        return connectToMySQL(db).query_db(query, new_user_dict)


    @classmethod
    def get_user_by_username(cls, user_dict):
        query = """
                SELECT * FROM users
                WHERE username = %(username)s;
                """
        result = connectToMySQL(db).query_db(query, user_dict)
        if result:
            user = User(result[0])
            return user


    @classmethod
    def get_user_by_id(cls, id):
        id_dict = {'id': id}
        query = """
                SELECT * FROM users
                WHERE id = %(id)s;
                """
        result = connectToMySQL(db).query_db(query, id_dict)
        if result:
            user = User(result[0])
            return user


    def set_password(self, user_dict):
        password_hash = generate_password_hash(user_dict['password'])
        username_and_password = {
                                'username': user_dict['username'],
                                'password_hash': password_hash
                                }
        self.password_hash = username_and_password['password_hash']
        query = """
                UPDATE users
                SET password_hash = %(password_hash)s
                WHERE username = %(username)s;
                """
        return connectToMySQL(db).query_db(query, username_and_password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


    def update_profile(self, current_user):
        query = """
                UPDATE users
                SET username = %(username)s,
                    about_me = %(about_me)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query, current_user)


    def record_last_seen(self, current_user):
        query = """
                UPDATE users
                SET last_seen = %(last_seen)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query, current_user)

class Card:

    def __init__(self, db_card):
        self.id = db_card['card_id']
        self.name = db_card['name']
        self.description = db_card['description']
        self.type = db_card['type']
        self.released_on = db_card['released_on']
        self.status = db_card['status']
        self.quantity = db_card['quantity']
        self.filename = db_card['filename']


    @classmethod
    def add_card(cls, new_card_dict):
        query = """
                INSERT INTO cards (
                    name,
                    description,
                    type,
                    released_on,
                    status,
                    quantity,
                    filename
                    )
                VALUES (
                    %(name)s,
                    %(description)s,
                    %(type)s,
                    NOW(),
                    %(status)s,
                    %(quantity)s,
                    %(filename)s
                    );
                """
        return connectToMySQL(db).query_db(query, new_card_dict)


    def like_card():
        pass


    def unlike_card():
        pass