from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine import *


class User(UserMixin, Document):
    username = StringField(required=True, max_length=64, unique=True, dbref=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)

    # Password Hashing
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Password Checking
    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get_user_by_username(cls, username):
        return cls.objects(username=username).first()

    @classmethod
    def get_user_by_email(cls, email):
        return cls.objects(email=email).first()
