from mongoengine import *


class MessageRoom(Document):
    _id = SequenceField(primary_key=True)
    senderName = StringField(required=True)
    receiverName = StringField(required=True)
    senderMessage = ListField(StringField())
    receiverMessage = ListField(StringField())
