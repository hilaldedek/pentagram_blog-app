from mongoengine import *
from app import app
from tests.confest import *
from werkzeug.security import generate_password_hash, check_password_hash


def test_user_password_hash():
    password = "password?.12_34"
    hashed_password = generate_password_hash(password)
    assert hashed_password is not None
    assert hashed_password != password
    assert check_password_hash(hashed_password, password) == True
    assert check_password_hash(hashed_password, "password?.12_3") == False


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


def test_user_logout(client):
    with app.test_client():
        new_user_create()
        response = client.post("/user/auth/login", json=first_user_login_data)
        assert response.status_code == 200
        response = client.post("/user/auth/logout", headers=create_headers(response))
        assert response.status_code == 200
