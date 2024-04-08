from mongoengine import *


class MessageRoom(Document):
    _id = SequenceField(primary_key=True)
    roomName = StringField(required=True)
    user1 = StringField(required=True)
    user2 = StringField(required=True)
