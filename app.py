from datetime import datetime
import os
import secrets
from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_login import UserMixin
from mongoengine import *
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models.post import Post
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
import requests
from config import config

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config.from_object(config)
jwt = JWTManager(app)
token_blacklist = set()

# DATABASE
client = MongoClient("mongodb://localhost:27017/?directConnection=true")
database = client["pentagram_db"]
collectionUser = database["user"]
collectionPost = database["post"]

connect("pentagram_db", host="mongodb://localhost:27017/?directConnection=true")

#Database Error Handling
try:
    connect("pentagram_db", host="mongodb://localhost:27017/?directConnection=true")
    print("succesfully connected!")
except Exception as error:
    print("unseccesfully process:", error)

if __name__ == "__main__":
    app.run(debug=True)

#Home Page
@app.route("/")
def home():
    return "Default Home Page"

#Login Page
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    results = collectionUser.find_one({"username": f"{username}"})
    if results is not None:
        if check_password_hash(results.get("password"), data.get("password")):
            #Token issued to logged in user
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200
        else:
            return (
                jsonify({"message": "Invalid password", "error": "invalid_password"}),
                401,
            )
    else:
        return jsonify({"message": "Invalid username"}), 401


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

#Register Page
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    new_user = User(
        username=data.get("username"),
        email=data.get("email"),
        password=data.get("password"),
    )
    new_user.set_password(data.get("password"))
    meta = {"collection": "user"}  #Collection name to save the user to
    new_user.save()
    login()
    access_token = create_access_token(identity=new_user.username)
    return jsonify({"message": "Data saved successfully", "access_token": access_token})

#Logout
@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    token_blacklist.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200

#Post Creation
@app.route("/post", methods=["POST"])
@jwt_required()
def post():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    new_post = Post(
        author=current_user_id,
        title=data.get("title"),
        content=data.get("content"),
        image=data.get("image"),
        dateTime=datetime.utcnow(),
    )
    meta = {"collection": "post"}  #Collection name to save the user to
    new_post.save()
    return jsonify({"message": "Post created successfully"})
