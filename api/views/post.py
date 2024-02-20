import os
from flask import jsonify, request
from pymongo import MongoClient
from mongoengine import *
from models.post import Post
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from flask_cors import cross_origin
from datetime import datetime
from flask_restful import Resource

client = MongoClient(
    os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
)
database = client["pentagram_db"]
collectionPost = database["post"]
collectionComment = database["comment_vote"]
collectionVote = database["vote"]
# try:
#     connect("pentagram_db", host="mongodb://localhost:27017/?directConnection=true")
# except Exception as error:
#     jsonify({"message": ConnectionError})


def get_formatted_post():
    posts = list(collectionPost.find().sort("dateTime", -1))
    formatted_posts = [
        {
            "_id": str(post["_id"]),
            "title": post["title"],
            "content": post["content"],
            "author": str(post["author"]),
            "dateTime": post["dateTime"].isoformat(),
            "like_counter": post["like_counter"],
            "dislike_counter": post["dislike_counter"],
        }
        for post in posts
    ]
    return formatted_posts


def get_post_detail_by_user(user_id, post_id):
    results = collectionPost.find(
        {"author": f"{user_id}", "_id": post_id}
    )  # The value from the url was searched in the database
    results_list = list(results)
    return results_list


class PostList(Resource):
    @cross_origin()
    def get(self):
        posts = get_formatted_post()
        return (jsonify({"posts": posts}), 200)


class PostCreate(Resource):
    @jwt_required()
    @cross_origin()
    def post(self):
        data = request.get_json()
        current_user_id = get_jwt_identity()  # current user
        new_post = Post(
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
        post_id = str(new_post.id)
        return jsonify({"message": "Post created successfully", "post_id": post_id})


class UserPost(Resource):
    @jwt_required()
    def get(self):
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


class PostDetail(Resource):
    @jwt_required()
    @cross_origin()
    def put(self, post_id):
        current_user_id = get_jwt_identity()
        results = get_post_detail_by_user(current_user_id, post_id)
        if results.__len__() != 0:
            data = request.get_json()
            collectionPost.update_one({"_id": post_id}, {"$set": data})
            return jsonify({"msg": "post updated successfully"}), 200
        else:
            return jsonify({"msg": "This post does not belong to you"}), 403

    @jwt_required()
    def delete(self, post_id):
        current_user_id = get_jwt_identity()
        results = get_post_detail_by_user(current_user_id, post_id)
        if results.__len__() != 0:
            collectionPost.delete_one(
                {"_id": post_id}
            )  # deleting the data whose id is given
            collectionComment.delete_many(
                {"postID": post_id}
            )  # If the post is deleted, the comments made on the post will be deleted.
            collectionVote.delete_many({"postID": post_id})
            return jsonify({"message": "Post deleted successfully"})
        else:
            return jsonify({"message": "Post is not found"})
