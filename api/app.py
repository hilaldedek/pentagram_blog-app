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
from models.comment_vote import Comment_vote
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
import requests
from config import config
import redis

ACCESS_EXPIRES = timedelta(hours=1)

app = Flask(__name__)

jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)
# Setup the Flask-JWT-Extended extension
app.config.from_object(config)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access"]
jwt = JWTManager(app) 
token_blacklist = set()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


# DATABASE
client = MongoClient("mongodb://localhost:27017/?directConnection=true")
database = client["pentagram_db"]
collectionUser = database["user"]
collectionPost = database["post"]
collectionComment_vote = database["comment_vote"]

connect("pentagram_db", host="mongodb://localhost:27017/?directConnection=true")

# Database Error Handling
try:
    connect("pentagram_db", host="mongodb://localhost:27017/?directConnection=true")
except Exception as error:
    jsonify({"message": ConnectionError})

if __name__ == "__main__":
    app.run(debug=True)


# Home Page
@app.route("/")
def home():
    return "Default Home Page"


def auto_increment_id():
    last_id = (
        collectionPost.find().sort({"_id": -1}).limit(1)
    )  # Finding the highest ID in the database
    last_id_list = list(last_id)
    new_id = last_id_list[0]["_id"] + 1  # id for new upcoming post
    return new_id


# Login Page
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    results = collectionUser.find_one(
        {"username": f"{username}"}
    )  # Searching the username entered by the user in the database
    if results is not None:
        # Checking the password if there is a username
        if check_password_hash(results.get("password"), data.get("password")):
            access_token = create_access_token(
                identity=username
            )  # Assigning a token to the user in the database
            return jsonify(access_token=access_token), 200
        else:
            return (
                jsonify({"message": "Invalid password", "error": "invalid_password"}),
                401,
            )
    else:
        return jsonify({"message": "Invalid username"}), 401


# Register Page
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    new_user = User(
        username=data.get("username"),
        email=data.get("email"),
        password=data.get("password"),
    )
    new_user.set_password(data.get("password"))  # password hashing
    meta = {"collection": "user"}  # Collection name to save the user to
    new_user.save()  # Saving the user to the database
    login()  # Ensuring that the registered user is logged in at the same time
    access_token = create_access_token(identity=new_user.username)  # !!
    return jsonify(
        {
            "message": "Data saved successfully and successfuly login",
            "access_token": access_token,
        }
    )


# Logout
@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt_identity()
    jwt_redis_blocklist.set(jti, "true", ex=app.config["JWT_ACCESS_TOKEN_EXPIRES"])
    return jsonify(message="cikis  basarili"), 200


# Post Creation
@app.route("/post", methods=["POST"])
@jwt_required()
def post():
    data = request.get_json()
    current_user_id = get_jwt_identity()  # current user
    new_post = Post(
        _id=auto_increment_id(),
        author=current_user_id,
        title=data.get("title"),
        content=data.get("content"),
        # image=request.files.get("image"),
        dateTime=datetime.utcnow(),
    )
    meta = {"collection": "post"}  # Collection name to save the user to
    new_post.save()
    return jsonify({"message": "Post created successfully"})


@app.route("/post-detail/<int:post_id>", methods=["DELETE", "PATCH", "GET"])
@jwt_required()
def detail_post(post_id):
    current_user_id = get_jwt_identity()  # current user
    results = collectionPost.find(
        {"author": f"{current_user_id}", "_id": post_id}
    )  # The value from the url was searched in the database
    print("RESULTS:", results)
    results_list = list(results)
    print("RESULT LIST: ", results_list)
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
        json_data = jsonify(results_list)

        if json_data is not None:
            return json_data
        else:
            return jsonify({"message": "Post is not found"})

    elif request.method == "PATCH":  #!!
        data = request.get_json()
        print("DATA: ", data)
        # ÇALIŞMIYOR
        for key, value in data.items():
            if key != "_id":
                results[key] = value
                collectionPost.update_one({"_id": post_id}, {"$set": results})


@app.route("/comment-vote/<int:post_id>", methods=["POST"])
@jwt_required()
def comment_vote(post_id):
    # Saving comments and votes on the post
    if request.method == "POST":
        data = request.get_json()
        current_user_id = get_jwt_identity()  # current user
        result = collectionPost.find_one({"_id": post_id})
        if result is not None:
            new_comment_vote = Comment_vote(
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


@app.route("/comment-vote/list", methods=["GET"])
def comment_vote_list_view():
    # All users can list comments and votes
    results = collectionComment_vote.find({}, projection={"_id": 0})
    results_list = list(results)
    json_data = results_list
    print(json_data)
    if json_data is not None:
        return jsonify(json_data)
    else:
        return jsonify({"message": "Post is not found"})


@app.route("/post/list", methods=["GET"])
def post_list_view():
    # All users can list all comments and votes
    results = list(collectionPost.find({}))
    print("RESULTS: ", results)
    json_data = jsonify(results)
    print(json_data)
    if json_data is not None:
        return json_data
