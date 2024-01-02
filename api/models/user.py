from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine import *


class User(UserMixin, Document):
    username = StringField(required=True, max_length=64, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)

    # unique_emails = set()
    # Password Hashing
    def get_user_with_username(self, username):
        if self.username == username:
            return self
        else:
            return None

    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Password Checking
    def check_password(self, password):
        return check_password_hash(self.password, password)