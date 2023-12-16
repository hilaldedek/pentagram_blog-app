from mongoengine import *
from models.user import User

class Post(Document):
    author = ReferenceField(User)
    title = StringField(required=True)
    content = StringField(required=True)
    image = ImageField()
    dateTime = DateTimeField()