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
from models.vote import Vote
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    set_access_cookies,
)
from config import config
from flask_cors import CORS, cross_origin
from datetime import datetime, timedelta, timezone

BLOCKLIST = set()

app = Flask(__name__)
CORS(app)


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
collectionComment = database["comment_vote"]
collectionToken = database["token_block_list"]
collectionVote = database["vote"]

connect("pentagram_db", host="mongodb://localhost:27017/?directConnection=true")

# Database Error Handling
try:
    connect("pentagram_db", host="mongodb://localhost:27017/?directConnection=true")
except Exception as error:
    jsonify({"message": ConnectionError})

if __name__ == "__main__":
    app.run(debug=True)


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_data):
    jti = jwt_data["jti"]
    token = collectionToken.find_one({"jti": jti})
    if token is not None:
        return jsonify({"message": "Token Blocklistte değil"})


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
        collectionComment.find().sort({"_id": -1}).limit(1)
    )  # Finding the highest ID in the database
    last_id_list = list(last_id)
    if last_id_list.__len__() == 0:
        new_id = 1
    else:
        new_id = last_id_list[0]["_id"] + 1  # id for new upcoming comment
    return new_id


# Home Page
@app.route("/", methods=["GET"])
@cross_origin()
def post_list_view():
    posts = list(collectionPost.find().sort("dateTime", -1))
    formatted_posts = [
        {
            "_id": str(post["_id"]),
            "title": post["title"],
            "content": post["content"],
            "author": str(post["author"]),
            "dateTime": post["dateTime"].isoformat(),
            "like_counter":post["like_counter"],
            "dislike_counter":post["dislike_counter"],
        }
        for post in posts
    ]

    return (jsonify({"posts": formatted_posts}), 200)


# Login Page
@app.route("/user/auth/login", methods=["POST"])
@cross_origin()
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
    # login()  # Ensuring that the registered user is logged in at the same time
    return jsonify({"message": "Data saved successfully and successfuly logged in"})


# Logout
@app.route("/user/auth/logout", methods=["POST"])
@jwt_required()
def logout():
    jwt = get_jwt()
    jti = jwt["jti"]
    token_b = TokenBlockList(jti=jti)
    token_b.save()
    if collectionToken.find({"jti": jti}):
        return jsonify({"message": "loged out successfully"}), 200
    else:
        return jsonify({"message": "Token is not on Blocklist"})


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
        like_counter=0,
        dislike_counter=0,

    )
    meta = {"collection": "post"}  # Collection name to save the user to
    new_post.save()
    return jsonify({"message": "Post created successfully"})


@app.route("/user/post", methods=["GET"])
@jwt_required()
def userPost():
    current_user_id = get_jwt_identity()
    results = collectionPost.find({"author": f"{current_user_id}"}).sort(
        "dateTime", -1
    )  # The value from the url was searched in the database
    results_list = list(results)
    json_data = jsonify(results_list)
    if json_data is not None:
        return json_data
    else:
        return jsonify({"message": "Posts is not found"})


@app.route("/post/<int:post_id>", methods=["DELETE", "PUT", "GET"])
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
            collectionComment.delete_many(
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

    elif request.method == "PUT":
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
            new_comment = Comment_vote(
                _id=auto_increment_id_for_comment(),
                person=current_user_id,
                postID=post_id,
                comment=data.get("comment"),
            )
            meta = {"collection": "comment_vote"}  # Collection name to save the user to
            new_comment.save()
            return jsonify({"message": "Comment saved successfully"})
        else:
            return jsonify({"message": "Post is not found"})


@app.route("/comment/<int:comment_id>", methods=["GET", "DELETE", "PUT"])
@jwt_required()
def comment_vote_detail(comment_id):
    current_user_id = get_jwt_identity()  # current user
    results_update = collectionComment.find(
        {"_id": comment_id, "person": f"{current_user_id}"}
    )
    results_list_update = list(results_update)
    if request.method == "GET":
        results_get_comment = collectionComment.find({"_id": comment_id})
        results_list_get = list(results_get_comment)
        json_data = jsonify(results_list_get)
        if json_data is not None:
            return json_data
        else:
            return jsonify({"message": "Comment is not found"})
    elif request.method == "PUT":
        if results_list_update.__len__() != 0:
            data = request.get_json()
            collectionComment.update_one({"_id": comment_id}, {"$set": data})
            return jsonify({"msg": "comment updated successfully"}), 200
        else:
            return jsonify({"msg": "This comment does not belong to you"})
    elif request.method == "DELETE":
        if results_list_update.__len__() != 0:
            collectionComment.delete_one(
                {"_id": comment_id}
            )  # deleting the data whose id is given
        return jsonify({"message": "Comment deleted successfully"})


@app.route("/comment-list/<int:post_id>", methods=["GET"])
def comment_vote_list_view(post_id):
    results = collectionComment.find({"postID": post_id})
    results_list = list(results)
    json_data = results_list
    if json_data is not None:
        return jsonify(json_data)
    else:
        return jsonify({"message": "Post is not found"})


@app.route("/post/<int:post_id>/vote", methods=["POST"])
@jwt_required()
def voteCounter(post_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()  # current user
    resultVote = collectionVote.find_one({"person": current_user_id, "postID": post_id})
    
    dataVote = data.get("vote")
    resultPost = collectionPost.find_one({"_id": post_id})
    current_like_counter = resultPost.get("like_counter", 0)
    current_dislike_counter = resultPost.get("dislike_counter", 0)
    if resultVote is not None:
        collectionVote.update_one(
            {"person": current_user_id, "postID": post_id}, {"$set": data}
        )
        if resultVote["vote"] == 1:
            if dataVote == -1:
                collectionPost.update_one(
                    {"_id": post_id},
                    {
                        "$set": {
                            "like_counter": current_like_counter - 1,
                            "dislike_counter": current_dislike_counter + 1,
                        }
                    },
                )
            elif dataVote == 0:
                collectionPost.update_one(
                    {"_id": post_id},
                    {"$set": {"like_counter": current_like_counter - 1}},
                )
        elif resultVote["vote"] == -1:
            if dataVote == 1:
                collectionPost.update_one(
                    {"_id": post_id},
                    {
                        "$set": {
                            "like_counter": current_like_counter + 1,
                            "dislike_counter": current_dislike_counter - 1,
                        }
                    },
                )
            elif dataVote == 0:
                collectionPost.update_one(
                    {"_id": post_id},
                    {"$set": {"dislike_counter": current_dislike_counter - 1}},
                )
        elif resultVote["vote"] == 0:
            if dataVote==1:
                collectionPost.update_one(
                    {"_id": post_id},
                    {"$set": {"like_counter": current_like_counter + 1}},
                )
            elif dataVote==-1:
                collectionPost.update_one(
                    {"_id": post_id},
                    {"$set": {"dislike_counter": current_dislike_counter +1}},
                )
    else:
        new_vote = Vote(
            person=current_user_id,
            postID=post_id,
            vote=data.get("vote"),
        )
        if dataVote == 1:
            collectionPost.update_one(
                {"_id": post_id},
                {"$set": {"like_counter": current_like_counter + 1}},
            )

        elif dataVote == -1:
            collectionPost.update_one(
                {"_id": post_id},
                {"$set": {"dislike_counter": current_dislike_counter + 1}},
            )
        meta = {"collection": "collectionVote"}  # Collection name to save the user to
        new_vote.save()
        return jsonify({"message": "vote saved successfully"})
    return jsonify()


# @app.route('/post/vote-list',methods=['GET'])
# @jwt_required()
# def getVoteList():