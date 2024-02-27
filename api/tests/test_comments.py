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


# User can view comments whether logged in or not
def test_get_user_comments(client):
    with app.test_client() as client:
        post_id = create_post().id
        create_comment(post_id)
        response = client.get(f"/comment-list/{post_id}")
        assert response.status_code == 200


def test_create_comment_not_logged_in():
    with app.test_client() as client:
        # if user is not logged in cannot create comment
        result = Post.objects.get()
        post_id = result.id
        response = client.post(f"/post/{post_id}/comment", json=post_data)
        assert response.status_code == 401


def test_create_comment_logged_in():
    with app.test_client() as client:
        new_user_create()
        response = client.post("/user/auth/login", json=first_user_login_data)
        assert response.status_code == 200
        post_id = create_post().id
        response_comment_create = client.post(
            f"/post/{post_id}/comment",
            json=comment_data2,
            headers=create_headers(response),
        )
        assert response_comment_create.status_code == 200


def test_update_comment_not_logged_in():
    with app.test_client() as client:
        result = Comment_vote.objects.get()
        comment_id = result.id
        response = client.put(f"/comment/{comment_id}", json=update_comment_data)
        assert response.status_code == 401


def test_update_comment_logged_in():
    with app.test_client() as client:
        new_user_create()
        response = client.post("/user/auth/login", json=first_user_login_data)
        assert response.status_code == 200
        post_id = create_post().id
        comment_id = create_comment(post_id).id
        response_comment_update = client.put(
            f"/comment/{comment_id}",
            headers=create_headers(response),
            json=update_comment_data,
        )
        assert response_comment_update.status_code == 200


def test_delete_comment_not_logged_in():
    with app.test_client() as client:
        result = Comment_vote.objects.first()
        comment_id = result.id
        response = client.put(f"/comment/{comment_id}", json=update_comment_data)
        assert response.status_code == 401


def test_delete_comment_logged_in():
    with app.test_client() as client:
        new_user_create()
        response = client.post("/user/auth/login", json=first_user_login_data)
        assert response.status_code == 200
        post_id = create_post().id
        comment_id = create_comment(post_id).id
        response_comment_delete = client.delete(
            f"/comment/{comment_id}",
            headers=create_headers(response),
        )
        assert response_comment_delete.status_code == 200
