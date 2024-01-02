from datetime import datetime, timedelta
import os
import secrets
from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_login import UserMixin
from mongoengine import *
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models.post import Post
from models.token import TokenBlockList
from models.comment_vote import Comment_vote
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
import requests
from config import config, BaseConfig
import redis

ACCESS_EXPIRES = timedelta(hours=1)
BLOCKLIST = set()

app = Flask(__name__)

# jwt_redis_blocklist = redis.StrictRedis(
#     host="localhost", port=6379, db=0, decode_responses=True
# )
# Setup the Flask-JWT-Extended extension
app.config.from_object(config)

jwt = JWTManager(app)


# DATABASE
client = MongoClient("mongodb://localhost:27017/?directConnection=true")
database = client["pentagram_db"]
collectionUser = database["user"]
collectionPost = database["post"]
collectionComment_vote = database["comment_vote"]
collectionToken = database["token_blocklist"]

connect("pentagram_db", host="mongodb://localhost:27017/?directConnection=true")

# Database Error Handling
try:
    connect("pentagram_db", host="mongodb://localhost:27017/?directConnection=true")
except Exception as error:
    jsonify({"message": ConnectionError})

if __name__ == "__main__":
    app.run(debug=True)

#JWT Error Handling
@jwt.expired_token_loader
def expired_token_callback(jwt_header,jwt_data):
    return jsonify({"message":"Token has expired","error":"token_expired"}),401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"message":"Signature verification failed","error":"invalid_token"})

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"message":"Request doesn't contain valid token","error":"authorization_header"})


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_data):
    jti=jwt_data["jti"]
    token=collectionToken.find_one({'jti':jti})
    return token is not None


# Function to give integer sequential id to incoming data
def auto_increment_id_for_post():
    last_id = (
        collectionPost.find().sort({"_id": -1}).limit(1)
    )  # Finding the highest ID in the database
    last_id_list = list(last_id)
    if last_id_list.__len__() == 0:
        new_id = 1
    else:
        new_id = last_id_list[0]["_id"] + 1  # id for new upcoming post
    return new_id


def auto_increment_id_for_comment():
    last_id = (
        collectionComment_vote.find().sort({"_id": -1}).limit(1)
    )  # Finding the highest ID in the database
    last_id_list = list(last_id)
    if last_id_list.__len__() == 0:
        new_id = 1
    else:
        new_id = last_id_list[0]["_id"] + 1  # id for new upcoming comment
    return new_id


# Home Page
@app.route("/", methods=["GET"])
def post_list_view():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("page", default=3, type=int)
    skip = (page - 1) * per_page
    posts = Post.objects.skip(skip).limit(per_page)
    formatted_posts = [
        {"_id": str(post["_id"]), 
         "title": post["title"], 
         "content": post["content"], 
         "dateTime": post["dateTime"].isoformat()
        }
        for post in posts
    ]

    return (
        jsonify({"posts": formatted_posts}),
        200
    )

# Login Page
@app.route("/user/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.get_user_by_username(username=data.get("username"))
    if user and (user.check_password(password=data.get("password"))):
        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)
        return (
            jsonify(
                {
                    "message": "Logged in",
                    "tokens": {
                        "access token": access_token,
                        "refresh token": refresh_token,
                    },
                }
            ),
            200,
        )
    return jsonify({"error": "Invalid username or password"}), 400


# Register Page
@app.route("/user/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    userCheckUsername = User.get_user_by_username(username=data.get("username"))
    userCheckEmail = User.get_user_by_email(email=data.get("email"))
    if userCheckUsername or userCheckEmail is not None:
        return jsonify({"error": "User already exist"})
    new_user = User(
        username=data.get("username"),
        email=data.get("email"),
        password=data.get("password"),
    )
    new_user.set_password(password=data.get("password"))  # password hashing
    meta = {"collection": "user"}  # Collection name to save the user to
    new_user.save()  # Saving the user to the database
    login()  # Ensuring that the registered user is logged in at the same time
    return jsonify({"message": "Data saved successfully and successfuly logged in"})


# Logout
@app.route("/user/auth/logout", methods=["POST"])
@jwt_required()
def logout():
    jwt=get_jwt()
    jti=jwt['jti']
    token_b=TokenBlockList(jti=jti)
    token_b.save()
    return jsonify({"message":"loged out successfully"}),200


# Post Creation
@app.route("/post", methods=["POST"])
@jwt_required()
def post():
    data = request.get_json()
    current_user_id = get_jwt_identity()  # current user
    new_post = Post(
        _id=auto_increment_id_for_post(),
        author=current_user_id,
        title=data.get("title"),
        content=data.get("content"),
        # image=request.files.get("image"),
        dateTime=datetime.utcnow(),
    )
    meta = {"collection": "post"}  # Collection name to save the user to
    new_post.save()
    return jsonify({"message": "Post created successfully"})


@app.route("/post/<int:post_id>", methods=["DELETE", "PATCH", "GET"])
@jwt_required()
def detail_post(post_id):
    current_user_id = get_jwt_identity()  # current user
    results = collectionPost.find(
        {"author": f"{current_user_id}", "_id": post_id}
    )  # The value from the url was searched in the database
    results_list = list(results)
    if request.method == "DELETE":
        if results_list.__len__() != 0:
            collectionPost.delete_one(
                {"_id": post_id}
            )  # deleting the data whose id is given
            collectionComment_vote.delete_many(
                {"postID": post_id}
            )  # If the post is deleted, the comments made on the post will be deleted.
            return jsonify({"message": "Post deleted successfully"})
        else:
            return jsonify({"message": "Post is not found"})
    elif request.method == "GET":
        results = collectionPost.find({"_id": post_id})
        results_list = list(results)
        json_data = jsonify(results_list)
        if json_data is not None:
            return json_data
        else:
            return jsonify({"message": "Post is not found"})

    elif request.method == "PATCH":
        if results_list.__len__() != 0:
            data = request.get_json()
            collectionPost.update_one({"_id": post_id}, {"$set": data})
            return jsonify({"msg": "post updated successfully"}), 200
        else:
            return jsonify({"msg": "This post does not belong to you"})


@app.route("/post/<int:post_id>/comment", methods=["POST"])
@jwt_required()
def comment_vote(post_id):
    # Saving comments and votes on the post
    if request.method == "POST":
        data = request.get_json()
        current_user_id = get_jwt_identity()  # current user
        result = collectionPost.find_one({"_id": post_id})
        if result is not None:
            new_comment_vote = Comment_vote(
                _id=auto_increment_id_for_comment(),
                person=current_user_id,
                postID=post_id,
                comment=data.get("comment"),
                vote=data.get("vote"),
            )
            print("POSTID: ", request.args.get("post_id"))
            meta = {"collection": "comment_vote"}  # Collection name to save the user to
            new_comment_vote.save()
            return jsonify({"message": "Comment Vote saved successfully"})
        else:
            return jsonify({"message": "Post is not found"})


@app.route("/comment/<int:comment_id>", methods=["GET", "DELETE", "PATCH"])
@jwt_required()
def comment_vote_detail(comment_id):
    current_user_id = get_jwt_identity()  # current user
    results_update = collectionComment_vote.find(
        {"_id": comment_id, "person": f"{current_user_id}"}
    )
    results_list_update = list(results_update)
    if request.method == "GET":
        results_get_comment = collectionComment_vote.find({"_id": comment_id})
        results_list_get = list(results_get_comment)
        json_data = jsonify(results_list_get)
        if json_data is not None:
            return json_data
        else:
            return jsonify({"message": "Comment is not found"})
    elif request.method == "PATCH":
        if results_list_update.__len__() != 0:
            data = request.get_json()
            collectionComment_vote.update_one({"_id": comment_id}, {"$set": data})
            return jsonify({"msg": "comment updated successfully"}), 200
        else:
            return jsonify({"msg": "This comment does not belong to you"})
    elif request.method == "DELETE":
        if results_list_update.__len__() != 0:
            collectionPost.delete_one(
                {"_id": comment_id}
            )  # deleting the data whose id is given
        return jsonify({"message": "Comment deleted successfully"})


# @app.route("/comment-vote/list", methods=["GET"])
# def comment_vote_list_view():
#     # All users can list comments and votes
#     results = collectionComment_vote.find({}, projection={"_id": 0})
#     results_list = list(results)
#     json_data = results_list
#     print(json_data)
#     if json_data is not None:
#         return jsonify(json_data)
#     else:
#         return jsonify({"message": "Post is not found"})


# @app.route("/post/list", methods=["GET"])
# def post_list_view():
#     # All users can list all comments and votes
#     results = list(collectionPost.find({}))
#     print("RESULTS: ", results)
#     json_data = jsonify(results)
#     print(json_data)
#     if json_data is not None:
#         return json_data
