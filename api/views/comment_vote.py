import json
from bson import ObjectId
from flask import jsonify, make_response, request
from mongoengine import *
from models.comment_vote import Comment_vote
from models.vote import Vote
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from flask_cors import cross_origin
from flask_restful import Resource
from models.post import Post
from models.user import User
from config import mongodb

mongodb()


class CommentCreate(Resource):
    @jwt_required()
    def post(self, post_id):
        # Saving comments and votes on the post
        if request.method == "POST":
            data = request.get_json()
            current_user_id = get_jwt_identity()  # current user
            result_post = Post.objects(_id=post_id).first()
            if result_post:
                current_user = User.objects(username=current_user_id).first()
                if current_user:
                    new_comment = Comment_vote(
                        person=current_user,
                        postID=result_post,
                        comment=data.get("comment"),
                    )
                    new_comment.save()
                    return make_response(
                        jsonify(
                            {"message": "Comment saved successfully", "status": "200"}
                        ),
                        200,
                    )
                else:
                    return make_response(
                        jsonify({"message": "User not found", "status": "404"}), 404
                    )
            else:
                return make_response(
                    jsonify({"message": "Post not found", "status": "404"}), 404
                )


class CommentDetail(Resource):
    @jwt_required()
    def get(self, comment_id):
        current_user_id = get_jwt_identity()
        current_user = User.objects(_id=current_user_id).first()
        comments = Comment_vote.objects(id=comment_id, person=current_user).first()
        if comments:
            return jsonify(comments.to_json())
        else:
            return make_response(
                jsonify({"message": "Comment is not found", "status": "404"}), 404
            )

    @jwt_required()
    @cross_origin()
    def put(self, comment_id):
        current_user_id = get_jwt_identity()
        current_user = User.objects(username=current_user_id).first()
        comments = Comment_vote.objects(_id=comment_id, person=current_user).first()
        if comments:
            data = request.get_json()
            comments.update(**data)
            return make_response(
                jsonify({"message": "Comment updated successfully", "status": "200"}),
                200,
            )
        else:
            return make_response(
                jsonify(
                    {"message": "This comment does not belong to you", "status": "403"}
                ),
                403,
            )

    @jwt_required()
    def delete(self, comment_id):
        current_user_id = get_jwt_identity()
        current_user = User.objects(username=current_user_id).first()
        comments = Comment_vote.objects(_id=comment_id, person=current_user).first()
        if comments:
            comments.delete()
            return make_response(
                jsonify({"message": "Comment deleted successfully", "status": "200"}),
                200,
            )
        else:
            return make_response(
                jsonify(
                    {"message": "This comment does not belong to you", "status": "403"}
                ),
                403,
            )


class CommentList(Resource):
    def get(self, post_id):
        comments = Comment_vote.objects(postID=post_id)
        formatted_comments = [
            {
                "_id": str(comment.id),
                "comment": comment.comment,
                "person": comment.person.username,
            }
            for comment in comments
        ]
        return make_response(
            jsonify({"comments": formatted_comments, "status": "200"}), 200
        )


class VoteProcedure(Resource):
    @jwt_required()
    @cross_origin()
    def post(self, post_id):
        data = request.get_json()
        current_username = get_jwt_identity()
        print(current_username)
        current_user = User.objects(username=current_username).first().id
        print(current_user, type(current_user))
        resultVote = Vote.objects(person=current_user, postID=post_id).first()
        dataVote = data.get("vote")
        resultPost = Post.objects(_id=post_id).first()
        resultPost_id = resultPost.id
        print(resultPost)

        if resultPost:
            current_like_counter = (
                resultPost.like_counter if resultPost.like_counter else 0
            )
            current_dislike_counter = (
                resultPost.dislike_counter if resultPost.dislike_counter else 0
            )
        else:
            current_like_counter = 0
            current_dislike_counter = 0

        if resultVote:
            resultVote.update(**data)
            if resultVote.vote == 1:
                if dataVote == -1:
                    resultPost.update(dec__like_counter=1, inc__dislike_counter=1)
                elif dataVote == 0:
                    resultPost.update(dec__like_counter=1)
            elif resultVote.vote == -1:
                if dataVote == 1:
                    resultPost.update(inc__like_counter=1, dec__dislike_counter=1)
                elif dataVote == 0:
                    resultPost.update(dec__dislike_counter=1)
            elif resultVote.vote == 0:
                if dataVote == 1:
                    resultPost.update(inc__like_counter=1)
                elif dataVote == -1:
                    resultPost.update(inc__dislike_counter=1)
        else:
            current_user = User.objects(username=current_username).first().id
            if dataVote == 1:
                Post.objects(_id=post_id).update(inc__like_counter=1)
            elif dataVote == -1:
                Post.objects(_id=post_id).update(inc__dislike_counter=1)
            new_vote = Vote(
                person=current_user,
                postID=resultPost_id,
                vote=dataVote,
            )
            new_vote.save()

        return make_response(
            jsonify({"message": "Vote saved successfully", "status": "200"}), 200
        )


class VoteList(Resource):
    @jwt_required()
    @cross_origin()
    def get(self):
        current_user_id = get_jwt_identity()
        votes = Vote.objects(person=current_user_id)
        return jsonify(votes.to_json())
