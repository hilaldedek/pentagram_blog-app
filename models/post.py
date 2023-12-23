from mongoengine import *
from models.user import User


class Post(Document):
    author = ReferenceField(User)
    title = StringField(required=True)
    content = StringField(required=True)
    image = ImageField(required=False)
    dateTime = DateTimeField()
    _id = IntField()
