import mongoengine
from models.user import User
import pytest
from pymongo import *

from pymongo import MongoClient
from mongoengine import connect

client = MongoClient("mongodb://localhost:27017/?directConnection=true")
db = client.pentagram_db
data = {
    "username": "fatih sultan mehmet",
    "email": "fsmehmet1453@gmail.com",
    "password": "fatih.1453!istanbul",
}

mongoengine.connect(
    db="pentagram_db",
    host="mongodb://localhost:27017/?directConnection=true",
    uuidRepresentation="standard",
)


def login_user(username, password):
    user = User.get_user_by_username(username=username)
    if user and user.check_password(password):
        return True
    return False


@pytest.fixture
def create_user():
    new_user = User(
        username=data.get("username"),
        email=data.get("email"),
        password=data.get("password"),
    )
    new_user.set_password(password=data.get("password"))
    meta = {"collection": "user"}
    new_user.save()
    yield new_user
    new_user.delete()


def test_user_register_and_login(create_user):
    assert login_user("fatih sultan mehmet", "fatih.1453!istanbul") == True
    assert (
        login_user("fatih sultan mehmet", "fatih.1453!.istanbul") == False
    )  # only password wrong
    assert (
        login_user("fatih2sultan mehmet", "fatih.1453!istanbul") == False
    )  # only username wrong
    assert (
        login_user("fatihsultan mehmet", "fatih.1453!.istanbul") == False
    )  # both are wrong
