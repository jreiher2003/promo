import os
from flask import Flask, url_for
from flask_login import LoginManager
from flask.ext.cache import Cache 
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt 

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
cache = Cache(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from app.users.views import users_blueprint
app.register_blueprint(users_blueprint)
from app.ascii.views import ascii_blueprint
app.register_blueprint(ascii_blueprint)

from app.users.models import Users 
from app.ascii.models import AsciiArt

login_manager.login_view = 'login'
login_manager.login_message = "You have to login first"
login_manager.login_message_category = "info"
@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter(Users.id == int(user_id)).one() 
