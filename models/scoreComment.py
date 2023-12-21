from mongoengine import *
from models.user import User


class scoreComment(Document):
    person = ReferenceField(User)
    score = IntField()
    comment = StringField()
