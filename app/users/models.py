import datetime 
from app import db, bcrypt, uploaded_photos 
from sqlalchemy.ext.hybrid import hybrid_property
from flask_security import UserMixin, RoleMixin

class Users(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    _password = db.Column(db.String)
    confirmed = db.Column(db.Boolean(), default=False)
    confirmed_at = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime,  default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    last_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(45))
    current_login_at = db.Column(db.DateTime)
    current_login_ip = db.Column(db.String(45))
    login_count = db.Column(db.Integer, default=0)
    asciiart = db.relationship("AsciiArt", lazy='subquery')
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic', cascade="all, delete-orphan", single_parent=True))

    @hybrid_property 
    def password(self):
        return self._password 

    @password.setter 
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_authenticated():
        return True

    def is_active():
        return True

    def is_anonymous():
        return False 

    def has_role(self, role):
        if role in self.roles:
            return True
        else:
            return False

    def get_id(self):
        return unicode(self.id)

# Define the Role DataModel
class Role(db.Model, RoleMixin):
    __tablename__ = "role"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Role %r>' % self.name

class UserRoles(db.Model):
    __tablename__ = "user_roles"
    
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), index=True)
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'), index=True)

