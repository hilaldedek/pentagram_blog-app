from mongoengine import *
from models.user import User


class Post(Document):
    _id = IntField()
    author = ReferenceField(User)
    title = StringField(required=True)
    content = StringField(required=True)
    image = ImageField(required=False)
    updated = BooleanField()
    dateTime = DateTimeField()
    updateTime = DateTimeField()
    like_counter=IntField(min_value=0)
    dislike_counter=IntField(min_value=0)
