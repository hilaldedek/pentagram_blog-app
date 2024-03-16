from mongoengine import *
from models.user import User


class Post(Document):
    _id = SequenceField(primary_key=True)
    author = ReferenceField(User)
    title = StringField(required=True)
    content = StringField(required=True)
    image = ImageField(required=False)
    updated = BooleanField()
    dateTime = DateTimeField()
    tags = ListField(StringField(max_length=20))
    like_counter = IntField(min_value=0)
    dislike_counter = IntField(min_value=0)
