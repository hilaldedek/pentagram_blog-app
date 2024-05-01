from mongoengine import *


class Message(Document):
    _id = SequenceField(primary_key=True)
    roomName = StringField(required=True)
    user1=StringField()
    user2=StringField()
    messages = ListField(StringField())
