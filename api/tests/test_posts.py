import json
from models.post import Post
from mongoengine import *
from app import app
from tests.confest import *


# The user can view posts on the home page whether he or she is logged in or not.
def test_get_all_post(client):
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "posts" in json.loads(response.data)

# POST VIEW
def test_post_view_not_logged_in(client):
    with app.test_client() as client:
        response = client.get("/user/post")
        assert response.status_code == 401


def test_post_view_logged_in(client):
    with app.test_client() as client:
        new_user_create()
        response_login = client.post("/user/auth/login", json=first_user_login_data)
        assert response_login.status_code == 200
        response = client.get("/user/post", headers=create_headers(response_login))
        assert response.status_code == 200

def test_post_detail_not_logged_in(client):
    with app.test_client() as client:
        new_user_create()
        post_id = create_post().id
        response = client.get(f"/post/{post_id}")
        assert response.status_code == 401


def test_post_detail_logged_in(client):
    with app.test_client() as client:
        new_user_create()
        response_login = client.post("/user/auth/login", json=first_user_login_data)
        assert response_login.status_code == 200
        post_id = create_post().id
        response = client.get(
            f"/post/{post_id}", headers=create_headers(response_login)
        )
        assert response.status_code == 200

def test_post_view_logged_in(client):
    with app.test_client() as client:
        new_user_create()
        response = client.post("/user/auth/login", json=first_user_login_data)
        assert response.status_code == 200
        response = client.get("/user/post", headers=create_headers(response))
        assert response.status_code == 200


# POST CREATE
def test_post_create_not_logged_in(client):
    # If the user is not logged in, she/he cannot create a new post.
    with app.test_client() as client:
        response = client.post("/post", data=post_data)
        assert response.status_code == 401


def test_post_create_logged_in(client):
    # If the user is logged in, she/he can create a new post.
    with app.test_client() as client:
        new_user_create()
        response = client.post("/user/auth/login", json=first_user_login_data)
        assert response.status_code == 200
        response = client.post(
            "/post", json=post_data, headers=create_headers(response)
        )
        assert response.status_code == 201


def test_update_post_not_logged_in(client):
    # If the user is not logged in, she/he cannot update her/his own post.
    with app.test_client() as client:
        post_id = create_post().id
        response_post_update = client.put(f"/post/{post_id}", json=update_post_data1)
        assert response_post_update.status_code == 401


def test_update_post_logged_in(client):
    with app.test_client() as client:
        new_user_create()
        response = client.post("/user/auth/login", json=first_user_login_data)
        assert response.status_code == 200
        post_id = create_post().id
        print(post_id)
        response_post_update = client.put(
            f"/post/{post_id}", json=update_post_data1, headers=create_headers(response)
        )
        assert response_post_update.status_code == 200


def test_update_another_post(client):
    with app.test_client() as client:
        new_user_create()
        response = client.post("/user/auth/login", json=first_user_login_data)
        assert response.status_code == 200
        post_id = create_post_user2().id
        response_post_update = client.put(
            f"/post/{post_id}", json=update_post_data2, headers=create_headers(response)
        )
        assert response_post_update.status_code == 403


def test_delete_post_not_logged_in(client):
    with app.test_client() as client:
        post_id = create_post().id
        response_post_delete = client.delete(f"/post/{post_id}")
        assert response_post_delete.status_code == 401


def test_delete_post_logged_in(client):
    with app.test_client() as client:
        new_user_create()
        response = client.post("/user/auth/login", json=first_user_login_data)
        assert response.status_code == 200
        post_id = create_post().id
        response_post_delete = client.delete(
            f"/post/{post_id}", headers=create_headers(response)
        )
        assert response_post_delete.status_code == 200


def test_delete_another_post(client):
    with app.test_client() as client:
        new_user_create()
        response = client.post("/user/auth/login", json=first_user_login_data)
        assert response.status_code == 200
        new_post = Post(
            author="user2",
            content=post_data.get("content"),
            title=post_data.get("title"),
        )
        new_post.save()
        post_id = new_post.id
        ("POST ID: ", post_id)
        response_post_delete = client.delete(
            f"/post/{post_id}", headers=create_headers(response)
        )
        assert response_post_delete.status_code == 403


def test_post_search(client):
    with app.test_client() as client:
        new_user_create()
        post_tags = create_post().tags[0]
        response_post_search = client.get(f"/tag/{post_tags}")
        assert response_post_search.status_code == 200
