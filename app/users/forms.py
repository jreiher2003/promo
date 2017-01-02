from flask_wtf import Form 
from wtforms import TextField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo 

class LoginForm(Form):
    username = TextField("Username", validators=[DataRequired(message="You need to put in a username"), Length(min=4, message="Your username need to be at least 4 characters long.")])
    password = PasswordField("Password", validators=[DataRequired(message="You need to enter a password"), Length(min=4,max=35, message="Your password needs to be between 4 and 35 chars")])
    remember_me = BooleanField("&nbsp;Remember Me")
    submit = SubmitField("Login")

class RegistrationForm(Form):
    username = TextField('Username', validators=[Length(min=4, max=25, message="Your username needs to be inbetween 4 and 25 chars")])
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('&nbsp;I accept the TOS', validators=[DataRequired(message="You need to accept the TOS.")])
    submit = SubmitField("Sign Up")