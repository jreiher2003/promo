import datetime
from flask.ext.testing import TestCase
from app import app, db, bcrypt
from app.models import AsciiArt, Users 


class BaseTestCase(TestCase):
    """A base test case."""
 
    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        user = Users(username='jeff',password=bcrypt.generate_password_hash('123456'))
        db.session.add(user)
        one = AsciiArt(
            title="test title",
            art="test art"
            )
        one.created=datetime.datetime.now()
        one.lat = 55.555
        one.lon = 55.555
        db.session.add(one)
        db.session.commit()
        

    def tearDown(self):
        db.session.remove()
        db.drop_all()