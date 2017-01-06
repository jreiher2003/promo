import os

class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SECRET_KEY = os.environ["SECRET_KEY"]
    CACHE_TYPE = "memcached"
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    # MAIL_DEFAULT_SENDER = '"Jeff" <jeffreiher@gmail.com>'
    # MAIL_SERVER = "mail.asciichan-tripplannr.com"
    # MAIL_PORT = 587
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ["MAIL_USERNAME"]
    MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]
    MAIL_DEFAULT_SENDER = '"Promo" <email@asciichan-tripplannr.com>'
    SECURITY_UNAUTHORIZED_VIEW = "/login/"
    SECURITY_MSG_UNAUTHORIZED = ("Try loging in first", "danger")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    UPLOADED_PHOTOS_DEST = "/vagrant/app/static/img"
    
class ProductionConfig(BaseConfig):
    DEBUG = False
    UPLOADED_PHOTOS_DEST = "/var/www/promo/img"