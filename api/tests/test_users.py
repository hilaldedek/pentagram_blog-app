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

post_data = {
    "title": "Snow-white",
    "content": "abc",
}
update_post_data1 = {
    "author": "user1",
    "title": "Cinderella",
    "content": "def",
}
update_post_data2 = {
    "author": "user2",
    "title": "Cinderella",
    "content": "def",
}

comment_data1 = {"person": "user1", "comment": "it's very nice!"}

comment_data2 = {"comment": "it's very nice!"}


update_comment_data = {"comment": "this comment updated!"}


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
        return new_user.username


def create_headers(response):
    access_token = json.loads(response.data)["tokens"]["access token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    return headers


def test_user_register(client):
    with app.test_client():
        response = client.post("/user/auth/register", json=first_user_data)
        assert response.status_code == 201


def test_duplicate_user_register(client):
    with app.test_client():
        new_user_create()
        response = client.post("/user/auth/register", json=first_user_data)
        assert response.status_code == 409


def test_user_login_successfuly(client):
    with app.test_client():
        new_user_create()
        response = client.post("/user/auth/login", json=first_user_login_data)
        assert response.status_code == 200


def test_user_login_failure(client):
    with app.test_client():
        new_user_create()
        response = client.post(
            "/user/auth/login", json=first_user_login_data_wrong_password
        )
        assert response.status_code == 400
        response = client.post(
            "/user/auth/login", json=first_user_login_data_wrong_username
        )
        assert response.status_code == 400
        response = client.post(
            "/user/auth/login", json=first_user_login_data_wrong_password_and_email
        )
        assert response.status_code == 400


# The user can view posts on the home page whether he or she is logged in or not.
def test_get_all_post(client):
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "posts" in json.loads(response.data)


# POST VIEW
def test_post_view(client):
    with app.test_client() as client:
        response = client.get("/user/post")
        assert response.status_code == 401
    with app.test_client() as client:
        new_user_create()
        response = client.post("/user/auth/login", json=first_user_login_data)
        assert response.status_code == 200
        response = client.get("/user/post", headers=create_headers(response))
        assert response.status_code == 200


# POST CREATE
def test_post_create(client):
    # If the user is not logged in, she/he cannot create a new post.
    with app.test_client() as client:
        response = client.post("/post", data=post_data)
        assert response.status_code == 401
    # If the user is logged in, she/he can create a new post.
    with app.test_client() as client:
        new_user_create()
        response = client.post("/user/auth/login", json=first_user_login_data)
        assert response.status_code == 200
        response = client.post(
            "/post", json=post_data, headers=create_headers(response)
        )
        # response_data = response.json
        # post_id = response_data.get("post_id")
        # print("RESPONSE DATA: ", post_id)
        assert response.status_code == 201


def test_update_post(client):
    # If the user is not logged in, she/he cannot update her/his own post.
    # with app.test_client() as client:
    #     response = client.put(f"/post/{post_id}", json=update_post_data)
    #     assert response.status_code == 401
    with app.test_client() as client:
        new_user_create()
        response = client.post("/user/auth/login", json=first_user_login_data)
        assert response.status_code == 200
        response_post_create = client.post(
            "/post", json=post_data, headers=create_headers(response)
        )
        assert response_post_create.status_code == 201
        post_id = json.loads(response_post_create.data)["post_id"]
        print("RESPONSE DATA: ", post_id)
        response_post_update = client.put(
            f"/post/{post_id}", json=update_post_data2, headers=create_headers(response)
        )
        assert response_post_update.status_code == 403
        # response = client.put(
        #     f"/post/{post_id}", json=update_post_data1, headers=headers
        # )
        # assert response.status_code == 200


def test_delete_post(client):
    with app.test_client() as client:
        new_user_create()
        response = client.post("/user/auth/login", json=first_user_login_data)
        assert response.status_code == 200
        response_post_create = client.post(
            "/post", json=post_data, headers=create_headers(response)
        )
        assert response_post_create.status_code == 201
        post_id = json.loads(response_post_create.data)["post_id"]
        response_post_delete = client.delete(
            f"/post/{post_id}", headers=create_headers(response)
        )
        assert response_post_delete.status_code == 200


# User can view comments whether logged in or not
def test_get_user_comments(client):
    with app.test_client() as client:
        new_post = Post(
            author=post_data.get("author"),
            content=post_data.get("content"),
            title=post_data.get("title"),
        )
        new_post.save()
        new_comment = Comment_vote(
            person=comment_data1.get("person"),
            postID=1,
            comment=comment_data1.get("comment"),
        )
        new_comment.save()
        result = Post.objects().first()
        post_id = result.id
        print(result.id)
        response = client.get(f"/comment-list/{post_id}")
        print(result.id)
        assert response.status_code == 200


def test_create_comment():
    # if user is not logged in cannot create comment
    with app.test_client() as client:
        result = Post.objects.get()
        post_id = result.id
        response = client.post(f"/post/{post_id}/comment", json=post_data)
        assert response.status_code == 401
        new_user_create()
        response = client.post("/user/auth/login", json=first_user_login_data)
        assert response.status_code == 200
        response_post_create = client.post(
            "/post", json=post_data, headers=create_headers(response)
        )
        assert response_post_create.status_code == 201
        post_id = json.loads(response_post_create.data)["post_id"]
        response_comment_create = client.post(
            f"/post/{post_id}/comment",
            json=comment_data2,
            headers=create_headers(response),
        )
        assert response_comment_create.status_code == 200


# def test_update_comment():
#     with app.test_client() as client:
#         result = Comment_vote.objects.get()
#         comment_id = result.id
#         response = client.put(f"/comment/{comment_id}", json=update_comment_data)
#         assert response.status_code == 401

#         new_post = Post(
#             _id=1,
#             author=first_user_data.get("username"),
#             content=post_data.get("content"),
#             title=post_data.get("title"),
#         )
#         new_post.save()
#         new_comment = Comment_vote(
#             person=first_user_data.get("username"),
#             postID=1,
#             comment=comment_data1.get("comment"),
#         )
#         new_comment.save()
#         user_created = new_user_create()
#         assert user_created == first_user_data.get("username")
#         response = client.post("/user/auth/login", json=first_user_login_data)
#         assert response.status_code == 200
#         result = Comment_vote.objects().first()
#         # print(result.person)
#         comment_id = result.id
#         response_comment_update = client.put(
#             f"/comment/{comment_id}",
#             json=update_comment_data,
#             headers=create_headers(response),
#         )
#         assert response_comment_update.status_code == 200
