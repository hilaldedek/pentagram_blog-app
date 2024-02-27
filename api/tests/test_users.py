import datetime
import json
import time
from flask import jsonify, session
import mongoengine
import requests
from models.comment_vote import Comment_vote
from models.user import User
from models.post import Post
from models.vote import Vote
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
from tests.test_data import *


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