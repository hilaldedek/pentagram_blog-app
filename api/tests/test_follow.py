from flask import app
from tests.confest import *


def test_get_follow_info_not_logged_in(client):
    with app.test_client() as client:
        response = client.get(f"/user/hilal/follow")
        assert response.status_code == 401


def test_get_follow_info_logged_in(client):
    with app.test_client() as client:
        new_user_create_3()
        username = new_user_create_2().username
        response_login = client.post("/user/auth/login", json=third_user_data)
        assert response_login.status_code == 200
        response = client.get(
            f"/user/{username}/follow", headers=create_headers(response_login)
        )
        assert response.status_code == 200


def test_get_follow_info_user_not_found(client):
    with app.test_client() as client:
        new_user_create()
        username = "hilal"
        response_login = client.post("/user/auth/login", json=first_user_login_data)
        assert response_login.status_code == 200
        response = client.get(
            f"/user/{username}/follow", headers=create_headers(response_login)
        )
        assert response.status_code == 404


def test_follow_not_logged_in(client):
    with app.test_client() as client:
        username = new_user_create_2().username
        response = client.post(f"/user/{username}/follow")
        assert response.status_code == 401


def test_follow_unfollow_logged_in(client):
    with app.test_client() as client:
        new_user_create()
        username2 = new_user_create_2().username
        username3 = new_user_create_3().username
        response_login = client.post("/user/auth/login", json=first_user_login_data)
        assert response_login.status_code == 200
        response = client.post(
            f"/user/{username2}/follow", headers=create_headers(response_login)
        )
        assert response.status_code == 200
        response = client.post(
            f"/user/{username3}/follow", headers=create_headers(response_login)
        )
        assert response.status_code == 200
        response = client.get(
            f"/user/{username2}/follow", headers=create_headers(response_login)
        )
        response_data = json.loads(response.data)
        assert "followInfo" in response_data
        follow_info = response_data["followInfo"]
        assert follow_info[0]["username"] == username2
        assert follow_info[0]["followStatus"] == 1
        assert follow_info[0]["follow"] == 0
        assert follow_info[0]["followers"] == 1
        assert response.status_code == 200
        response_unfollow = client.put(
            f"/user/{username2}/follow", headers=create_headers(response_login)
        )
        assert response_unfollow.status_code == 200
        response_unfollow = client.put(
            f"/user/{username3}/follow", headers=create_headers(response_login)
        )
        assert response_unfollow.status_code == 200


def test_follow_unfollow_user_not_found(client):
    with app.test_client() as client:
        new_user_create()
        username = "hilal"
        response_login = client.post("/user/auth/login", json=first_user_login_data)
        assert response_login.status_code == 200
        response = client.post(
            f"/user/{username}/follow", headers=create_headers(response_login)
        )
        assert response.status_code == 404
        response_unfollow = client.put(
            f"/user/{username}/follow", headers=create_headers(response_login)
        )
        assert response_unfollow.status_code == 404


def test_unfollow_not_logged_in(client):
    with app.test_client() as client:
        username = new_user_create_2().username
        response = client.put(f"/user/{username}/follow")
        assert response.status_code == 401


def test_not_follow_user(client):
    with app.test_client() as client:
        new_user_create()
        username = new_user_create_2().username
        response_login = client.post("/user/auth/login", json=first_user_login_data)
        assert response_login.status_code == 200
        response_unfollow = client.put(
            f"/user/{username}/follow", headers=create_headers(response_login)
        )
        assert response_unfollow.status_code == 404


def test_get_user_profile_posts_not_logged_in(client):
    with app.test_client() as client:
        new_user_create()
        username = new_user_create_2().username
        response = client.get(f"/user/{username}/post")
        assert response.status_code == 401


def test_get_user_profile_posts_logged_in(client):
    with app.test_client() as client:
        new_user_create()
        username = new_user_create_2().username
        response_login = client.post("/user/auth/login", json=first_user_login_data)
        assert response_login.status_code == 200
        response = client.get(
            f"/user/{username}/post", headers=create_headers(response_login)
        )
        assert response.status_code == 200


def test_get_user_profile_posts_user_not_found(client):
    with app.test_client() as client:
        new_user_create()
        username = "hilal"
        response_login = client.post("/user/auth/login", json=first_user_login_data)
        assert response_login.status_code == 200
        response = client.get(
            f"/user/{username}/post", headers=create_headers(response_login)
        )
        assert response.status_code == 404
