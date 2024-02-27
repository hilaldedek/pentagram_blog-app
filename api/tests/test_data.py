import json
from models.comment_vote import Comment_vote
from models.post import Post
from models.user import User



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
    "author": "user1",
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

comment_data1 = {"comment": "it's very nice!"}

comment_data2 = {"comment": "it's very nice!"}


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
        return new_user.username


def create_post():
    new_post = Post(
        author=post_data.get("author"),
        content=post_data.get("content"),
        title=post_data.get("title"),
    )
    new_post.save()
    return new_post


def create_comment(post_id):
    new_comment = Comment_vote(
        person=first_user_data.get("username"),
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
