import pytest
import json
from models.comment_vote import Comment_vote
from models.user import User
from models.post import Post
from models.vote import Vote
from mongoengine import *
from app import app
import mongomock


@pytest.fixture()
def client():
    disconnect()
    connect(
        "mongoenginetest",
        host="localhost",
        mongo_client_class=mongomock.MongoClient,
        uuidRepresentation="standard",
    )
    app.config.update(
        {
            "TESTING": True,
        }
    )
    with app.test_client() as client:
        yield client


first_user_data = {
    "username": "user1",
    "email": "example@gmail.com",
    "password": "test1",
}
first_user_login_data = {
    "username": "user1",
    "password": "test1",
}
first_user_login_data_wrong_username = {
    "username": "user12",
    "password": "test1",
}
first_user_login_data_wrong_password = {
    "username": "user1",
    "password": "test12",
}
first_user_login_data_wrong_password_and_email = {
    "username": "user12",
    "password": "test12",
}
second_user_data = {
    "username": "user2",
    "email": "example2@gmail.com",
    "password": "test2",
}
third_user_data = {
    "username": "user3",
    "email": "example3@gmail.com",
    "password": "test3",
}

post_data = {
    "author": 1,
    "title": "Snow-white",
    "content": "abc",
    "tags": ["Python", "vue", "python", "flask"],
}

post_data2 = {
    "author": 2,
    "title": "def",
    "content": "abc",
    "tags": ["flask", "python", "dedek"],
}

update_post_data1 = {
    "title": "Cinderella",
    "content": "def",
    "tags": ["Css", "Vue", "python"],
}

update_post_data2 = {
    "title": "Cinderella",
    "content": "def",
    "tags": ["flask", "python", "mongo"],
}

comment_data1 = {"comment": "it's very nice!"}

comment_data2 = {"comment": "very nice!"}


update_comment_data = {"comment": "this comment updated!"}

vote_data = {"vote": 1}


def new_user_create():
    existing_user = User.objects(email=first_user_data.get("email")).first()
    if existing_user:
        return existing_user.username
    else:
        new_user = User(
            username=first_user_data.get("username"),
            email=first_user_data.get("email"),
            password=first_user_data.get("password"),
        )
        new_user.set_password(password=first_user_data.get("password"))
        new_user.save()
        return new_user.id


def new_user_create_2():
    existing_user = User.objects(email=second_user_data.get("email")).first()
    if existing_user:
        return existing_user.username
    else:
        new_user = User(
            username=second_user_data.get("username"),
            email=second_user_data.get("email"),
            password=second_user_data.get("password"),
        )
        new_user.set_password(password=second_user_data.get("password"))
        new_user.save()
        return new_user


def new_user_create_3():
    existing_user = User.objects(email=third_user_data.get("email")).first()
    if existing_user:
        return existing_user.username
    else:
        new_user = User(
            username=third_user_data.get("username"),
            email=third_user_data.get("email"),
            password=third_user_data.get("password"),
        )
        new_user.set_password(password=third_user_data.get("password"))
        new_user.save()
        return new_user

def new_user_create_2():
    existing_user = User.objects(email=second_user_data.get("email")).first()
    if existing_user:
        return existing_user.username
    else:
        new_user = User(
            username=second_user_data.get("username"),
            email=second_user_data.get("email"),
            password=second_user_data.get("password"),
        )
        new_user.set_password(password=second_user_data.get("password"))
        new_user.save()
        return new_user
    
def new_user_create_3():
    existing_user = User.objects(email=third_user_data.get("email")).first()
    if existing_user:
        return existing_user.username
    else:
        new_user = User(
            username=third_user_data.get("username"),
            email=third_user_data.get("email"),
            password=third_user_data.get("password"),
        )
        new_user.set_password(password=third_user_data.get("password"))
        new_user.save()
        return new_user

def create_post():
    new_post = Post(
        author=post_data.get("author"),
        content=post_data.get("content"),
        title=post_data.get("title"),
        tags=post_data.get("tags"),
    )
    new_post.save()
    return new_post


def create_post_user2():
    new_post = Post(
        author=post_data2.get("author"),
        content=post_data2.get("content"),
        title=post_data2.get("title"),
        tags=post_data2.get("tags"),
    )
    new_post.save()
    return new_post


def create_comment(post_id):
    new_comment = Comment_vote(
        person=post_data.get("author"),
        postID=post_id,
        comment=comment_data1.get("comment"),
    )
    new_comment.save()
    return new_comment


def create_headers(response):
    access_token = json.loads(response.data)["tokens"]["access token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    return headers
