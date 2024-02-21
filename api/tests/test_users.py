import datetime
import json
import time
from flask import jsonify, session
import mongoengine
import requests
from models.comment_vote import Comment_vote
from models.user import User
from models.post import Post
import pytest
from mongoengine import *
from views.post import (
    PostList,
    PostCreate,
    PostDetail,
    UserPost,
)
from app import app
import mongomock


@pytest.fixture()
def client():
    disconnect()
    connect(
        "mongoenginetest", host="localhost", mongo_client_class=mongomock.MongoClient
    )
    app.config.update(
        {
            "TESTING": True,
        }
    )
    with app.test_client() as client:
        yield client


first_user_data = {
    "username": "fatihsultan",
    "email": "fsmehmet1453@gmail.com",
    "password": "fatih.1453!istanbul",
}
first_user_login_data = {
    "username": "fatihsultan",
    "password": "fatih.1453!istanbul",
}
second_user_data = {
    "username": "yavuzsultanselim",
    "email": "ysselim@gmail.com",
    "password": "yavuz.123sultan!selim",
}

post_data = {
    "title": "Snow-white",
    "content": "abc",
}
update_post_data = {
    "title": "Cinderella",
    "content": "def",
}

comment_data = {"comment": "it's very nice!"}

update_comment_data = {"comment": "this comment updated!"}


@pytest.fixture
def test_user():
    user = User(username="user1", email="test@example.com", password="test")
    user.save()
    return user


@pytest.fixture
def test_post_1():
    post = Post(content="test_post1", title="test post 1", author="user1")
    post.save()
    return post


@pytest.fixture
def test_post_2():
    post = Post(content="test_post2", title="test post 2", author="user2")
    post.save()
    return post


@pytest.fixture()
def register_user(client):
    with app.test_client() as client:
        register_response = client.post("/user/auth/register", json=first_user_data)
        if register_response.status_code == 200:
            return jsonify({"message": "User registration successfully."}), 200
        else:
            return None


@pytest.fixture()
def login_user(test_user, client):
    with app.test_client() as client:
        print(test_user.username)
        login_response = client.post(
            "/user/auth/login", json={"username": "user1", "password": "test"}
        )
        print("login_response: ", login_response)
        if login_response.status_code == 200:
            access_token = login_response.json["tokens"]["access token"]
            return access_token
        else:
            return None


@pytest.fixture()
def create_post(client, login_user):
    with app.test_client() as client:
        access_token = login_user
        headers = {"Authorization": f"Bearer {access_token}"}
        post_response = client.post("/post", json=post_data, headers=headers)
        if post_response.status_code == 200:
            return json.loads(post_response)
        else:
            return jsonify({"error": "Posting failed"}), 400


def test_user_login_and_register(client, login_user):
    with app.test_client():
        assert login_user is not None


# The user can view posts on the home page whether he or she is logged in or not.
def test_get_formatted_post(client):
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "posts" in json.loads(response.data)


# POST CREATE
def test_post_create(client, login_user, create_post):
    # If the user is not logged in, she/he cannot create a new post.
    with app.test_client() as client:
        response = client.post("/post", data=post_data)
        assert response.status_code == 401
    # If the user is logged in, she/he can create a new post.
    with app.test_client() as client:
        if login_user:
            create_post_response = create_post
            print(create_post_response)
            create_post_response_to_json = json.loads(create_post_response)
            assert create_post_response_to_json.status_code == 200


# # If the user is not logged in, she/he cannot view her/his own post.
# def test_get_user_posts():
#     with app.test_client() as client:
#         response = client.get("/user/post")
#         assert response.status_code == 401


# def test_update_post(create_user):

#     with app.test_client() as client:
#         login_response = client.post(
#             "/user/auth/login",
#             json={
#                 "username": first_user_data.get("username"),
#                 "password": first_user_data.get("password"),
#             },
#         )
#         assert login_response.status_code == 200
#         access_token = json.loads(login_response.data)["tokens"]["access token"]
#         headers = {
#             "Authorization": f"Bearer {access_token}",
#             "Content-Type": "application/json",
#         }
#         response = client.post("/post", json=post_data, headers=headers)
#         print("RESPONSE: ", json.loads(response.data)["post_id"])
#         assert response.status_code == 200
#         post_id = json.loads(response.data)["post_id"]
#         response = client.put(
#             f"/post/{post_id}", json=update_post_data, headers=headers
#         )
#         assert response.status_code == 200
#     # If the user is not logged in, she/he cannot update her/his own post.
#     with app.test_client() as client:
#         response = client.put(f"/post/{post_id}", json=update_post_data)
#         assert response.status_code == 401
#     # The user cannot update a post that does not belong to him/her.
#     with app.test_client() as client:
#         register_response = client.post(
#             "/user/auth/register",
#             json=first_user_data,
#         )
#         assert register_response.status_code == 200
#         login_response = client.post(
#             "/user/auth/login",
#             json={
#                 "username": second_user_data.get("username"),
#                 "password": second_user_data.get("password"),
#             },
#         )
#         assert login_response.status_code == 200
#         access_token = json.loads(login_response.data)["tokens"]["access token"]
#         headers = {"Authorization": f"Bearer {access_token}"}
#         response = client.put(
#             f"/post/{post_id}", json=update_post_data, headers=headers
#         )
#         assert response.status_code == 403


# def test_delete_post(register_user, login_user):
#     # If the user is not logged in, the delete operation cannot be performed.
#     with app.test_client() as client:
#         result = Post.objects()
#         post_id = result.id
#         response = client.delete(f"/post/{result.id}")
#         assert response.status_code == 401

#     with app.test_client() as client:
#         register_response = register_user()
#         assert register_response.status_code == 200
#         login_response = login_user()
#         assert login_response.status_code == 200
#         access_token = json.loads(login_response.data)["tokens"]["access token"]
#         headers = {"Authorization": f"Bearer {access_token}"}
#         result = Post.objects(author=first_user_data.get("username"))
#         print(result)
#         post_id = result.id
#         response = client.delete(f"/post/{post_id}", headers=headers)
#         assert response.status_code == 200


# # User can view comments whether logged in or not
# def test_get_user_comments():
#     with app.test_client() as client:
#         result = User.objects(username=first_user_data.get("username"))
#         print(result)
#         post_id = result.id
#         response = client.get(f"/comment-list/{post_id}")
#         assert response.status_code == 200


# def test_create_comment(create_user):
#     # if user is not logged in cannot create comment
#     with app.test_client() as client:
#         result = Post.objects.get()
#         post_id = result.id
#         response = client.post(f"/post/{post_id}/comment", json=post_data)
#         assert response.status_code == 401


# def test_update_comment():
#     with app.test_client() as client:
#         result = Comment_vote.objects.get()
#         comment_id = result.id
#         response = client.put(f"/comment/{comment_id}", json=update_comment_data)
#         assert response.status_code == 401
