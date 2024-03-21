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

from flask import Flask
from mongoengine import *
from flask_jwt_extended import JWTManager
import mongoengine
from config import config
from flask_cors import CORS
from flask_restful import Api
from views.user import *
from views.post import *
from views.comment_vote import *
from dotenv import load_dotenv
from config import mongodb

app = Flask(__name__)
CORS(app, supports_credentials=True, origins="*")
api = Api(app)
app.config.from_object(config)

jwt = JWTManager(app)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")


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


if __name__ == "__main__":
    mongodb()
    app.run(debug=True, host="0.0.0.0")
