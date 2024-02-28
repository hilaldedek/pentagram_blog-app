from mongoengine import *
from app import app
from tests.confest import *


def test_vote_list_not_logged_in():
    with app.test_client() as client:
        response = client.get(f"/post/vote_list")
        assert response.status_code == 401


def test_vote_list_logged_in():
    with app.test_client() as client:
        new_user_create()
        response = client.post("/user/auth/login", json=first_user_login_data)
        assert response.status_code == 200
        response = client.get(f"/post/vote_list", headers=create_headers(response))
        assert response.status_code == 200


def test_create_vote_not_logged_in():
    with app.test_client() as client:
        post_id = create_post().id
        response = client.post(f"/post/{post_id}/vote")
        assert response.status_code == 401


def test_create_vote_logged_in():
    with app.test_client() as client:
        new_user_create()
        response = client.post("/user/auth/login", json=first_user_login_data)
        assert response.status_code == 200
        post_id = create_post().id
        response_vote_create = client.post(
            f"/post/{post_id}/vote",
            json=vote_data,
            headers=create_headers(response),
        )
        assert response_vote_create.status_code == 200
