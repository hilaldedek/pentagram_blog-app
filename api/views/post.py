from flask import jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin
from datetime import datetime
from flask_restful import Resource
from models.post import Post
from models.user import User
from config import mongodb

mongodb()
class PostList(Resource):
    @cross_origin()
    def get(self):
        posts = Post.objects.order_by("-dateTime").all()
        formatted_posts = [
            {
                "_id": str(post.id),
                "title": post.title,
                "content": post.content,
                "author": post.author.username,
                "dateTime": post.dateTime.isoformat(),
                "like_counter": post.like_counter,
                "dislike_counter": post.dislike_counter,
            }
            for post in posts
        ]
        return make_response(jsonify({"posts": formatted_posts, "status": "200"}), 200)


class PostCreate(Resource):
    @jwt_required()
    @cross_origin()
    def post(self):
        data = request.get_json()
        current_user_id = get_jwt_identity()
        current_user = User.objects(username=current_user_id).first()
        if current_user:
            new_post = Post(
                author=current_user,
                title=data.get("title"),
                content=data.get("content"),
                dateTime=datetime.utcnow(),
                like_counter=0,
                dislike_counter=0,
            )
            new_post.save()
            return make_response(
                jsonify(
                    {
                        "message": "Post created successfully",
                        "post_id": str(new_post.id),
                        "status": "201",
                    }
                ),
                201,
            )
        else:
            return make_response(
                jsonify({"message": "User not found", "status": "404"}), 404
            )


class UserPost(Resource):
    @jwt_required()
    def get(self):
        current_username = get_jwt_identity()
        current_user = User.objects(username=current_username).first()
        if current_user:
            posts = Post.objects(author=current_user.id).order_by("-dateTime").all()
            formatted_posts = [
                {
                    "_id": str(post.id),
                    "title": post.title,
                    "content": post.content,
                    "author": post.author.username,
                    "dateTime": post.dateTime.strftime("%d %m %Y %H %M %S"),
                    "like_counter": post.like_counter,
                    "dislike_counter": post.dislike_counter,
                }
                for post in posts
            ]
            print("USER POST LIST: ", formatted_posts)
            return make_response(
                jsonify({"posts": formatted_posts, "status": "200"}), 200
            )
        else:
            return make_response(
                jsonify({"message": "User not found", "status": "404"}), 404
            )


class PostDetail(Resource):
    @jwt_required()
    @cross_origin()
    def put(self, post_id):
        current_user_id = get_jwt_identity()
        current_user = User.objects(username=current_user_id).first()
        post = Post.objects(_id=post_id, author=current_user).first()
        if post:
            data = request.get_json()
            post.modify(**data)
            return make_response(
                jsonify({"message": "Post updated successfully", "status": "200"}), 200
            )
        else:
            return jsonify({"msg": "This post does not belong to you"})

    @jwt_required()
    def delete(self, post_id):
        current_user_id = get_jwt_identity()
        current_user = User.objects(username=current_user_id).first()
        post = Post.objects(_id=post_id, author=current_user).first()
        if post:
            post.delete()
            return make_response(
                jsonify({"message": "Post deleted successfully", "status": "200"}), 200
            )
        else:
            return jsonify({"message": "Post is not found"})
