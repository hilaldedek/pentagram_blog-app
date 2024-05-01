from mongoengine import *


class TokenBlockList(Document):
    _id = SequenceField(primary_key=True)
    jti = StringField()
    created_at = DateTimeField()

    def __repr__(self):
        return f"<Token {self.jti}>"
