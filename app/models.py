import datetime # pragma: no cover
from app import db # pragma: no cover

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

class AsciiArt(db.Model):
    
    __tablename__ = 'asciiart'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    art = db.Column(db.String)
    created = db.Column(db.Date, default=datetime.datetime.now())
    lon = db.Column(db.Float)
    lat = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("Users", lazy='subquery')

    @property 
    def format_date(self):
        return '{dt:%A} {dt:%B} {dt.day}, {dt.year}'.format(dt=self.created)

    def __repr__(self):
        return '<title>: {}'.format(self.title)