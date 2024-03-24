from datetime import timedelta
import os

from dotenv import load_dotenv
from mongoengine import connect


def mongodb():
    load_dotenv()
    mongo_uri = os.environ.get("MONGO_URI")
    print(mongo_uri)
    connect(host=mongo_uri, alias="default")


class BaseConfig(object):
    DEBUG = False
    JWT_SECRET_KEY = "!6uad-[aadşawlmdşwaödDArKZ8zp0V3bfXzWxW:ffhn7JlszRG9e;d6-HcCya"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


config = DevelopmentConfig
