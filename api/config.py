from datetime import timedelta


class BaseConfig(object):
    DEBUG = False
    JWT_SECRET_KEY = "!6uad-[aadşawlmdşwaödDArKZ8zp0V3bfXzWxW:ffhn7JlszRG9e;d6-HcCya"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


config = DevelopmentConfig
