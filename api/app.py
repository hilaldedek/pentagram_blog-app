"""
Pentagram Flask Backend

This Flask application serves as the backend for the Pentagram project. It provides various API endpoints for user authentication, post management, comment handling, and voting.

API Endpoints:
- `/`: GET method, retrieves a list of posts sorted by date in descending order.
- `/user/auth/login`: POST method, user login with username and password.
- `/user/auth/register`: POST method, user registration with username, email, and password.
- `/user/auth/logout`: POST method, user logout with JWT authentication.
- `/post`: POST method, creates a new post with title, content, and author information.
- `/user/post`: GET method, retrieves posts created by the authenticated user.
- `/post/<int:post_id>`: GET, PUT, DELETE methods, retrieves, updates, or deletes a specific post.
- `/post/<int:post_id>/comment`: POST method, adds a comment to a specific post.
- `/comment/<int:comment_id>`: GET, PUT, DELETE methods, retrieves, updates, or deletes a specific comment.
- `/comment-list/<int:post_id>`: GET method, retrieves a list of comments for a specific post.
- `/post/<int:post_id>/vote`: POST method, handles voting (like, dislike) on a specific post.

Dependencies:
- Flask
- Flask-Login
- Flask-JWT-Extended
- Flask-CORS
- MongoDB with MongoEngine

Note: The backend is configured to run with a MongoDB database. Make sure to set up the MongoDB connection before running the application.

"""

import os
import threading
from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from mongoengine import *
from flask_jwt_extended import JWTManager
import mongoengine
from models.message_room import MessageRoom
from views.follow import FollowUser, UserProfilePostList
from config import config
from flask_cors import CORS
from flask_restful import Api
from views.user import *
from views.post import *
from views.comment_vote import *
from views.chat import *
from models.message import Message
from config import mongodb

app = Flask(__name__)
CORS(app, supports_credentials=True, origins="*", host=8000)
api = Api(app)
app.config.from_object(config)

jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")

lock = threading.Lock()
room_users = {}


@socketio.on("first_connect")
def handle_connect(msg):
    print("User connected")


@socketio.on("connect_error")
def error_handler(e):
    print("Error occurred:", e)


@socketio.on("join")
def on_join(data):
    username = data["username"]
    currentUsername = data["currentUser"]
    room = data["room"]
    roomUsers = []
    messageRoom = MessageRoom.objects(roomName=room).first()
    if messageRoom:
        join_room(room)
        with lock:
            if room not in room_users:
                room_users[room] = [currentUsername]
            else:
                room_users[room].append(currentUsername)
    else:
        new_room = MessageRoom(user1=currentUsername, user2=username, roomName=room)
        new_room.save()
        join_room(room)
        with lock:
            if room not in room_users:
                room_users[room] = [currentUsername]
            else:
                room_users[room].append(currentUsername)


@socketio.on("leave")
def on_leave(data):
    username = data["currentUsername"]
    room = data["room"]
    leave_room(room)
    with lock:
        if room in room_users and username in room_users[room]:
            room_users[room].remove(username)


@socketio.on("new_message")
def handle_new_message(data):
    currentUsername = data.get("currentUsername")
    username = data.get("username")
    message = data.get("message")
    room = data.get("room")
    messageRoom1 = MessageRoom.objects(roomName=room).first()

    if messageRoom1:
        dbData = []
        data = {"username": currentUsername, "message": message}
        dbData.append(f"{currentUsername}:{message}")
        print(dbData)
        emit("response", data, to=room)
        with lock:
            if username not in room_users.get(room, []):
                data="Yeni bir mesajınız var"
                emit("notification",data , to=username)
        pass
        message = Message.objects(roomName=room).first()
        if message:
            updated_messages = message.messages + dbData
            message.update(messages=updated_messages)
        else:
            new_message = Message(
                roomName=room, user1=currentUsername, user2=username, messages=dbData
            )
            new_message.save()
        print(f"{currentUsername} message: ", message, f"{room}")


api.add_resource(Login, "/user/auth/login")
api.add_resource(Logout, "/user/auth/logout")
api.add_resource(Register, "/user/auth/register")
api.add_resource(PostList, "/")
api.add_resource(PostCreate, "/post")
api.add_resource(UserPost, "/user/post")
api.add_resource(PostDetail, "/post/<int:post_id>")
api.add_resource(CommentCreate, "/post/<int:post_id>/comment")
api.add_resource(CommentDetail, "/comment/<int:comment_id>")
api.add_resource(CommentList, "/comment-list/<int:post_id>")
api.add_resource(VoteProcedure, "/post/<int:post_id>/vote")
api.add_resource(VoteList, "/post/vote_list")
api.add_resource(PostSearch, "/tag/<string:post_tag>")
api.add_resource(FollowUser, "/user/<string:username>/follow")
api.add_resource(UserProfilePostList, "/user/<string:username>/post")
api.add_resource(MessageHistory, "/chat/<string:username>")

if __name__ == "__main__":
    mongodb()
    socketio.run(debug=True, host="0.0.0.0")
