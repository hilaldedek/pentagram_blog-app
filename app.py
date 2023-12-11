from flask import Flask, jsonify, request
from pymongo import MongoClient
import pymongo
from flask_login import UserMixin
from mongoengine import *
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

# DATABASE
connect("deneme", host="mongodb://localhost:27017/?directConnection=true")
try:
    connect("deneme", host="mongodb://localhost:27017/?directConnection=true")
    print("succesfully connected!")
except Exception as error:
    print("unseccesfully process:", error)

if __name__ == "__main__":
    app.run(debug=True)


# MODELS
class User(UserMixin, Document):
    username = StringField(required=True, max_length=64, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    # unique_emails = set()
    # Password Hashing

    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Password Checking
    def check_password(self, password):
        return check_password_hash(self.password, password)


@app.route("/")
def home():
    return "Home Page"


@app.route("/login")
def login():
    return "Login Page"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.get_json()
        new_user = User(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password"),
        )
        new_user.set_password(data.get("password"))
        new_user.save()
        return jsonify({"message": "Data saved successfully"})

    return "Register Page"
