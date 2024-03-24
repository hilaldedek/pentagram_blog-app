from flask import jsonify, make_response, request
from models.post import Post
from models.user import User
from models.follow import Follow
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from flask_cors import cross_origin
from flask_restful import Resource
from config import mongodb


mongodb()


class FollowUser(Resource):
    @jwt_required()
    def get(self, username):
        current_user = get_jwt_identity()
        current_user_db = Follow.objects(username=current_user).first()
        username_id = User.objects(username=username).first()
        user_db = Follow.objects(username=username).first()
        if username_id is not None:
            if user_db is not None:
                if current_user_db is not None:
                    db_follow_list = current_user_db.follow
                    if user_db is not None:
                        user_db_followers_list = user_db.followers
                        user_db_follow_list = user_db.follow
                        if username_id.id in db_follow_list:
                            followInfo = [
                                {
                                    "username": username,
                                    "followStatus": 1,
                                    "follow": len(user_db_follow_list),
                                    "followers": len(user_db_followers_list),
                                }
                            ]
                            return make_response(jsonify({"followInfo": followInfo}))
                        else:
                            followInfo = [
                                {
                                    "username": username,
                                    "followStatus": 0,
                                    "follow": len(user_db_follow_list),
                                    "followers": len(user_db_followers_list),
                                }
                            ]

                            return make_response(jsonify({"followInfo": followInfo}))
            else:
                followInfo = [
                    {
                        "username": username,
                        "followStatus": 0,
                        "follow": 0,
                        "followers": 0,
                    }
                ]
                return make_response(jsonify({"followInfo": followInfo}))
        else:
            return make_response(
                jsonify({"message": f"{username} is not found.", "status": "404"}),
                404,
            )

    @jwt_required()
    def post(self, username):
        current_user = get_jwt_identity()
        current_username_id = User.objects(username=current_user).first()
        username_id = User.objects(username=username).first()
        if username_id is None:
            return make_response(
                jsonify({"message": f"{username} is not found.", "status": "404"}),
                404,
            )
        follow_list = [username_id.id]
        followers_list = [current_username_id.id]
        current_user_db = Follow.objects(username=current_user).first()
        user_db = Follow.objects(username=username).first()
        if current_user_db is not None:
            db_follow_list = current_user_db.follow
            if db_follow_list:
                merged_list = list(set(current_user_db.follow + follow_list))
                current_user_db.update(follow=merged_list)
            else:
                current_user_db.update(follow=follow_list)
        else:
            follow = Follow(username=current_user, follow=follow_list)
            follow.save()
        if user_db is not None:
            db_followers_list = user_db.followers
            if db_followers_list:
                merged_list = list(set(user_db.followers + followers_list))
                user_db.update(followers=merged_list)
            else:
                user_db.update(followers=followers_list)
        else:
            follower = Follow(username=username, followers=followers_list)
            follower.save()
        return make_response(
            jsonify(
                {"message": f"{username} was followed successfully.", "status": "200"}
            ),
            200,
        )

    @jwt_required()
    def put(self, username):
        current_user = get_jwt_identity()
        current_username_id = User.objects(username=current_user).first()
        username_id = User.objects(username=username).first()
        if username_id is None:
            return make_response(
                jsonify({"message": f"{username} is not found.", "status": "404"}),
                404,
            )
        current_user_db = Follow.objects(username=current_user).first()
        user_db = Follow.objects(username=username).first()
        if current_user_db is not None:
            current_user_db_follow_list = current_user_db.follow
            current_user_db_followers_list = current_user_db.followers
            print(username_id.id in current_user_db_follow_list)
            if username_id.id in current_user_db_follow_list:
                current_user_db_follow_list.remove(username_id.id)
                current_user_db.update(follow=current_user_db_follow_list)
                user_db_followers_list = user_db.followers
                user_db_follow_list = user_db.follow
                if current_username_id.id in user_db_followers_list:
                    user_db_followers_list.remove(current_username_id.id)
                    user_db.update(followers=user_db_followers_list)
                    if (
                        len(user_db_follow_list) == 0
                        and len(user_db_followers_list) == 0
                    ):
                        user_db.delete()
                if (
                    len(current_user_db_follow_list) == 0
                    and len(current_user_db_followers_list) == 0
                ):
                    current_user_db.delete()
                return make_response(
                    jsonify(
                        {
                            "message": f"{current_user} unfollowed {username}.",
                            "status": "200",
                        }
                    ),
                    404,
                )
            else:
                return make_response(
                    jsonify(
                        {
                            "message": f"{current_user} does not follow {username}.",
                            "status": "404",
                        }
                    ),
                    404,
                )
        else:
            return make_response(
                jsonify(
                    {
                        "message": f"{current_user} is not found",
                        "status": "404",
                    }
                ),
                404,
            )


class UserProfilePostList(Resource):
    @jwt_required()
    def get(self, username):
        user = User.objects(username=username).first()
        if user:
            posts = Post.objects(author=user.id).order_by("-dateTime").all()
            formatted_posts = [
                {
                    "_id": str(post.id),
                    "title": post.title,
                    "content": post.content,
                    "author": post.author.username,
                    "dateTime": post.dateTime.strftime("%d %m %Y %H %M %S"),
                    "tags": post.tags,
                    "like_counter": post.like_counter,
                    "dislike_counter": post.dislike_counter,
                }
                for post in posts
            ]
            return make_response(
                jsonify({"posts": formatted_posts, "status": "200"}), 200
            )
        else:
            return make_response(
                jsonify({"message": "User not found", "status": "404"}), 404
            )
