from mongoengine import *
from models.user import User


class Follow(Document):
    _id = SequenceField(primary_key=True)
    username = ReferenceField(User)
    followers = ListField(IntField())
    follow = ListField(IntField())
