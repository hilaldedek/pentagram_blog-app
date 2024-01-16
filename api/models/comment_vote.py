from mongoengine import *
from models.user import User
from models.post import Post


class Comment_vote(Document):
    _id = IntField()
    person = ReferenceField(User)
    postID = ReferenceField(Post)
    vote = BooleanField()
    comment = StringField()
    updated=BooleanField()
