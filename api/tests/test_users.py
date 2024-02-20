import json
import mongoengine
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

mongoengine.disconnect()
mongoengine.connect(
    db="mongoenginetest",
    host="localhoste",
    uuidRepresentation="standard",
    mongo_client_class=mongomock.MongoClient,
)
conn = mongoengine.get_db()

first_user_data = {
    "username": "fatih sultan",
    "email": "fsmehmet1453@gmail.com",
    "password": "fatih.1453!istanbul",
}
second_user_data = {
    "username": "yavuz sultan selim",
    "email": "ysselim@gmail.com",
    "password": "yavuz.123sultan!selim",
}

post_data = {
    "title": "Snow-white",
    "content": "It was the middle of winter, and the snow-flakes were falling like feathers from the sky, and a queen sat at her window working, and her embroidery-frame was of ebony. And as she worked, gazing at times out on the snow, she pricked her finger, and there fell from it three drops of blood on the snow. And when she saw how bright and red it looked, she said to herself, Oh that I had a child as white as snow, as red as blood, and as black as the wood of the embroidery frame! Not very long after she had a daughter, with a skin as white as snow, lips as red as blood, and hair as black as ebony, and she was named Snow-white. And when she was born the queen died.",
}
update_post_data = {
    "title": "Cinderella",
    "content": "There was once a rich man whose wife lay sick, and when she felt her end drawing near she called to her only daughter to come near her bed, and said, Dear child, be pious and good, and God will always take care of you, and I will look down upon you from heaven, and will be with you. And then she closed her eyes and expired. The maiden went every day to her mother's grave and wept, and was always pious and good. When the winter came the snow covered the grave with a white covering, and when the sun came in the early spring and melted it away, the man took to himself another wife",
}

comment_data = {"comment": "it's very nice!"}


def login_user(username, password):
    user = User.get_user_by_username(username=username)
    if user and user.check_password(password):
        return True
    return False


@pytest.fixture
def create_user():
    new_user = User(
        username=first_user_data.get("username"),
        email=first_user_data.get("email"),
        password=first_user_data.get("password"),
    )
    new_user.set_password(password=first_user_data.get("password"))
    meta = {"collection": "user"}
    new_user.save()
    yield new_user
    new_user.delete()


def test_user_login(create_user):
    with app.test_client() as client:
        response = client.post(
            "/user/auth/login",
            json={
                "username": first_user_data.get("username"),
                "password": first_user_data.get("password"),
            },
        )
        assert response.status_code == 200


# The user can view posts on the home page whether he or she is logged in or not.
def test_get_formatted_post():
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "posts" in json.loads(response.data)


# POST CREATE
def test_post_create(create_user):
    # If the user is not logged in, she/he cannot create a new post.
    with app.test_client() as client:
        response = client.post("/post", json=post_data)
        assert response.status_code == 401
    # If the user is logged in, she/he can create a new post.
    with app.test_client() as client:
        response = client.post(
            "/user/auth/login",
            json={
                "username": first_user_data.get("username"),
                "password": first_user_data.get("password"),
            },
        )
        assert response.status_code == 200
        access_token = json.loads(response.data)["tokens"]["access token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.post("/post", json=post_data, headers=headers)
        assert response.status_code == 200


# If the user is not logged in, she/he cannot view her/his own post.
def test_get_user_posts():
    with app.test_client() as client:
        response = client.get("/user/post")
        assert response.status_code == 401


# def test_update_post(create_user):
#     # If the user is not logged in, she/he cannot update her/his own post.
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
#         headers = {"Authorization": f"Bearer {access_token}"}
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


def test_delete_post(create_user):
    # If the user is not logged in, the delete operation cannot be performed.
    with app.test_client() as client:
        result = Post.objects.get()
        response = client.delete(f"/post/{result.id}")
        assert response.status_code == 401

    # with app.test_client() as client:
    #     login_response = client.post(
    #         "/user/auth/login",
    #         json={
    #             "username": first_user_data.get("username"),
    #             "password": first_user_data.get("password"),
    #         },
    #     )
    #     assert login_response.status_code == 200
    #     access_token = json.loads(login_response.data)["tokens"]["access token"]
    #     headers = {"Authorization": f"Bearer {access_token}"}
    #     result = Post.objects.get(author=first_user_data.get("username"))
    #     post_id = result.id
    #     response = client.delete(f"/post/{post_id}", headers=headers)
    #     assert response.status_code == 200


def test_create_comment(create_user):
    with app.test_client() as client:
        result = Post.objects.get()
        post_id = result.id
        response = client.post(f"/post/{post_id}/comment", json=post_data)
        assert response.status_code == 401
    with app.test_client() as client:
        login_response = client.post(
            "/user/auth/login",
            json={
                "username": first_user_data.get("username"),
                "password": first_user_data.get("password"),
            },
        )
        assert login_response.status_code == 200

        # access_token = json.loads(login_response.data)["tokens"]["access token"]
        # headers = {"Authorization": f"Bearer {access_token}"}
        # response = client.post(
        #     f"/post/{post_id}/comment", json=comment_data, headers=headers
        # )
        # assert response.status_code == 200
