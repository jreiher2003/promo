import datetime 
from app import db 

class Users(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    asciiart = db.relationship("AsciiArt", lazy='subquery')

    def is_authenticated():
        return True

    def is_active():
        return True

    def is_anonymous():
        return False 

    def get_id(self):
        return unicode(self.id)
