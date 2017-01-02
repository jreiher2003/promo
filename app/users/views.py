from app import app, db, cache, bcrypt 
from app.users.forms import LoginForm, RegistrationForm
from app.users.models import Users 
from flask import render_template, url_for, redirect, request, Blueprint, flash
from flask_login import login_user, logout_user, login_required, current_user

users_blueprint = Blueprint("users", __name__, template_folder="templates")

@users_blueprint.route("/login", methods=["GET","POST"])
def login():
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        remember_me = form.remember_me.data
        if user is not None and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=remember_me)
            flash("You just logged in as %s!" % user.username, "success")
            return redirect(url_for('ascii.hello'))
        else:
            flash("<strong>Invalid password.</strong> Please try again.", "danger")
            return redirect(url_for("users.login"))
    return render_template("login.html", form=form, error=error)

@users_blueprint.route("/", methods=["GET","POST"])
def signup():
    error = None
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(
            username=form.username.data,
            password=bcrypt.generate_password_hash(form.password.data)
            )
        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("You have just signup up congrats!", "success")
            return redirect(url_for("hello"))
        except:
            flash("That username already exists", "danger")
            return redirect(url_for("users.signup"))
    return render_template("signup.html", form=form, error=error)

@users_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You just successfully logged out", "danger")
    return redirect(url_for('users.signup'))