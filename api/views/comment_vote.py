import os
from flask import jsonify, request
from pymongo import MongoClient
from mongoengine import *
from models.comment_vote import Comment_vote
from models.vote import Vote
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from flask_cors import cross_origin
from flask_restful import Resource

client = MongoClient(os.getenv("MONGO_URI","mongodb://localhost:27017/?directConnection=true"))
database = client["pentagram_db"]
collectionPost = database["post"]
collectionComment = database["comment_vote"]
collectionVote = database["vote"]
# try:
#     connect("pentagram_db", host="mongodb://localhost:27017/?directConnection=true")
# except Exception as error:
#     jsonify({"message": ConnectionError})


def get_comment_detail_by_user(comment_id, user_id):
    results_update = collectionComment.find({"_id": comment_id, "person": f"{user_id}"})
    results_list_update = list(results_update)
    return results_list_update


class CommentCreate(Resource):
    @jwt_required()
    def post(self, post_id):
        # Saving comments and votes on the post
        if request.method == "POST":
            data = request.get_json()
            current_user_id = get_jwt_identity()  # current user
            result = collectionPost.find_one({"_id": post_id})
            if result is not None:
                new_comment = Comment_vote(
                    person=current_user_id,
                    postID=post_id,
                    comment=data.get("comment"),
                )
                meta = {
                    "collection": "comment_vote"
                }  # Collection name to save the user to
                new_comment.save()
                return jsonify({"message": "Comment saved successfully"}),200
            else:
                return jsonify({"message": "Post is not found"}),404


class CommentDetail(Resource):
    @jwt_required()
    def get(self, comment_id):
        current_user_id = get_jwt_identity()
        comments = get_comment_detail_by_user(comment_id, current_user_id)
        json_data = jsonify(comments)

        if json_data is not None:
            return json_data
        else:
            return jsonify({"message": "Comment is not found"})

    @jwt_required()
    @cross_origin()
    def put(self, comment_id):
        current_user_id = get_jwt_identity()
        comments = get_comment_detail_by_user(comment_id, current_user_id)
        if comments.__len__() != 0:
            data = request.get_json()
            collectionComment.update_one({"_id": comment_id}, {"$set": data})
            return jsonify({"msg": "comment updated successfully"}), 200
        else:
            return jsonify({"msg": "This comment does not belong to you"})

    @jwt_required()
    def delete(self, comment_id):
        current_user_id = get_jwt_identity()
        comments = get_comment_detail_by_user(comment_id, current_user_id)
        if comments.__len__() != 0:
            collectionComment.delete_one(
                {"_id": comment_id}
            )  # deleting the data whose id is given
        return jsonify({"message": "Comment deleted successfully"})


class CommentList(Resource):
    def get(self, post_id):
        results = collectionComment.find({"postID": post_id})
        results_list = list(results)
        json_data = results_list
        if json_data is not None:
            return jsonify(json_data)
        else:
            return jsonify({"message": "Post is not found"})


class VoteProcedure(Resource):
    @jwt_required()
    @cross_origin()
    def post(self, post_id):
        data = request.get_json()
        current_user_id = get_jwt_identity()  # current user
        resultVote = collectionVote.find_one(
            {"person": current_user_id, "postID": post_id}
        )
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
            meta = {
                "collection": "collectionVote"
            }  # Collection name to save the user to
            new_vote.save()
            return jsonify({"message": "vote saved successfully"})
        return jsonify()


class VoteList(Resource):
    @jwt_required()
    @cross_origin()
    def get(self):
        current_user_id = get_jwt_identity()
        results = collectionVote.find({"person": current_user_id}, {"_id": 0})
        results_list = list(results)
        json_data = results_list
        if json_data is not None:
            return jsonify(json_data)
        else:
            return jsonify({"message": "Vote data is not found"})
