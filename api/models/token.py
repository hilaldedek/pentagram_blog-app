from mongoengine import *

class TokenBlockList(Document):
    id=IntField()
    jti=StringField()
    created_at=DateTimeField()


    def __repr__(self):
        return f"<Token {self.jti}>"