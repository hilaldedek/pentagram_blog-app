import os
import secrets
from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_login import UserMixin
from mongoengine import *
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
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
collection = database["user"]

connect("pentagram_db", host="mongodb://localhost:27017/?directConnection=true")

try:
    connect("pentagram_db", host="mongodb://localhost:27017/?directConnection=true")
    print("succesfully connected!")
except Exception as error:
    print("unseccesfully process:", error)

if __name__ == "__main__":
    app.run(debug=True)


@app.route("/")
def home():
    return "Default Home Page"


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    results = collection.find_one({"username": f"{username}"})
    if results is not None:
        if check_password_hash(results.get("password"), data.get("password")):
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


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    new_user = User(
        username=data.get("username"),
        email=data.get("email"),
        password=data.get("password"),
    )
    new_user.set_password(data.get("password"))
    new_user.save()
    print("USER REGISTER")
    login()
    access_token = create_access_token(identity=new_user.username)
    return jsonify({"message": "Data saved successfully", "access_token": access_token})


@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    token_blacklist.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200
