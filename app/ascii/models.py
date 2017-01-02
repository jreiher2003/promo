import datetime # pragma: no cover
from app import db # pragma: no cover

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