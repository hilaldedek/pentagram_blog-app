import json
from flask import jsonify, make_response
from flask_cors import cross_origin
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from models.message import Message


class MessageHistory(Resource):
    @jwt_required()
    @cross_origin()
    def get(self, username):
        current_user_id = get_jwt_identity()
        nameList=[username,current_user_id]
        sortedNameList=sorted(nameList)
        roomName = f"{sortedNameList[0]}_{sortedNameList[1]}_rooms"
        messageHistory1 = Message.objects(roomName=roomName).first()
        if messageHistory1:
            response_data = {
                "id": str(messageHistory1.id),
                "roomName": messageHistory1.roomName,
                "messages": messageHistory1.messages
            }
            return make_response(
                jsonify(
                    {
                        "messageHistory": response_data,
                        "status": "200",
                    }
                ),
                200,
            )
        else:
            return make_response(
                jsonify(
                    {
                        "messageHistory": "",
                        "status": "200",
                    }
                ),
                200,
            )
