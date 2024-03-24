from mongoengine import *
from models.user import User
from models.post import Post


class Vote(Document):
    _id = SequenceField(primary_key=True)
    person = ReferenceField(User)
    postID = ReferenceField(Post)
    vote = IntField()