from flask_wtf import Form 
from wtforms import TextField, SubmitField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class LoginForm(Form):
    email = EmailField("Email", validators=[DataRequired(message="You need to put in a username"), Email()])
    password = PasswordField("Password", validators=[DataRequired(message="You need to enter a password"), Length(min=4,max=35, message="Your password needs to be between 4 and 35 chars")])
    remember_me = BooleanField("&nbsp;Remember Me")
    submit = SubmitField("Login")

class RegistrationForm(Form):
    email = EmailField("Email", validators=[DataRequired(message="You need to put in a username"), Email()])
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('&nbsp;I accept the TOS', validators=[DataRequired(message="You need to accept the TOS.")])
    submit = SubmitField("Sign Up")

class RecoverPasswordForm(Form):
    email = EmailField("Email", [DataRequired(), Email()])
    submit = SubmitField("Reset Password")

class ChangePasswordTokenForm(Form):
    password = PasswordField("Password", [DataRequired(), Length(min=12, message="The min password length is 12 chars long.")])
    password_confirm = PasswordField("Confirm", [DataRequired(), EqualTo("password", message="Your passwords don't match.")])
    submit = SubmitField("Change Password")