from flask import Flask, jsonify, request
from pymongo import MongoClient
import pymongo
from flask_login import UserMixin
from mongoengine import *
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

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


# MODELS
class User(UserMixin, Document):
    username = StringField(required=True, max_length=64, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)

    # unique_emails = set()
    # Password Hashing
    def get_user_with_username(self, username):
        if self.username == username:
            return self
        else:
            return None

    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Password Checking
    def check_password(self, password):
        return check_password_hash(self.password, password)


@app.route("/")
def home():
    return "Home Page"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        results = collection.find_one({"username": f"{username}"})
        if results is not None:
            if check_password_hash(results.get("password"), data.get("password")):
                print("USER LOGIN")
            else:
                print("PASSWORD WRONG")
        else:
            print("USER NOT FOUND")
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
        print("USER REGISTER")
        login()
        return jsonify({"message": "Data saved successfully"})
    return "Register Page"
