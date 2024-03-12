from flask import jsonify, make_response, request
from models.user import User
from models.token import TokenBlockList
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
)
from flask_cors import cross_origin
from flask_restful import Resource
from config import mongodb

mongodb()


class Login(Resource):
    @cross_origin()
    def post(self):
        data = request.get_json()
        user = User.get_user_by_username(username=data.get("username"))
        if user and (user.check_password(password=data.get("password"))):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)
            return (
                jsonify(
                    {
                        "message": "Logged in",
                        "tokens": {
                            "access token": access_token,
                            "refresh token": refresh_token,
                        },
                    }
                ),
                200,
            )
        return jsonify({"error": "Invalid username or password"}), 400


class Register(Resource):
    def post(self):
        data = request.get_json()
        userCheckUsername = User.get_user_by_username(username=data.get("username"))
        userCheckEmail = User.get_user_by_email(email=data.get("email"))
        if userCheckUsername or userCheckEmail is not None:
            return make_response(
                jsonify({"message": "User already exist", "status": "409"}), 409
            )
        new_user = User(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password"),
        )
        new_user.set_password(password=data.get("password"))  # password hashing
        new_user.save()  # Saving the user to the database
        return make_response(
            jsonify({"message": "User registration successfully.", "status": "201"}),
            201,
        )


class Logout(Resource):
    @jwt_required()
    @cross_origin()
    def post(self):
        jwt = get_jwt()
        jti = jwt["jti"]
        token_b = TokenBlockList(jti=jti)
        token_b.save()
        if TokenBlockList.objects(jti=jti):
            return jsonify({"message": "loged out successfully", "status": "200"}), 200
        else:
            return (
                jsonify({"message": "Token is not on Blocklist", "status": "404"}),
                404,
            )
