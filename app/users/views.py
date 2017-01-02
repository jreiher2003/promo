from app import app, db, cache, bcrypt 
from app.users.forms import LoginForm, RegistrationForm
from app.users.models import Users, UserRoles
from flask import render_template, url_for, redirect, request, Blueprint, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.users.utils import get_ip, is_safe_url, generate_confirmation_token, confirm_token, \
send_email, password_reset_email

users_blueprint = Blueprint("users", __name__, template_folder="templates")

@users_blueprint.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is not None and bcrypt.check_password_hash(user.password,form.password.data):
            remember_me = form.remember_me.data
            user.login_count += 1
            user.last_login_ip = user.current_login_ip
            user.last_login_at = user.current_login_at
            user.current_login_ip = get_ip()
            user.current_login_at = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()
            cache.clear()
            login_user(user, remember=remember_me)
            next = request.args.get("next")
            if not is_safe_url(next):
                return flask.abort(400)
            flash("You just logged in as %s!" % user.username, "success")
            return redirect(url_for('ascii.hello'))
        else:
            flash("<strong>Invalid password.</strong> Please try again.", "danger")
            return redirect(url_for("users.login"))
    return render_template("login.html", form=form)

@users_blueprint.route("/", methods=["GET","POST"])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(
            email=form.email.data,
            password = form.password.data,
            login_count = 1,
            current_login_ip = get_ip(),
            current_login_at = datetime.datetime.now()
            )
        try:
            db.session.add(user)
            db.session.commit()
            cache.clear()
            token = generate_confirmation_token(user1.email)
            confirm_url = url_for('users.confirm_email_register', token=token, _external=True)
            html = render_template("security/email/welcome.html", confirm_url=confirm_url, user=user1)
            subject = "Please confirm your email"
            send_email(user1.email, subject, html)
            login_user(user)
            flash("You have just signup up congrats!", "success")
            next = request.args.get("next")
            if not is_safe_url(next):
                return flask.abort(400)
            return redirect(next or url_for("hello"))
        except:
            flash("That username already exists", "danger")
            return redirect(url_for("users.signup"))
    return render_template("signup.html", form=form)

@users_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You just successfully logged out", "danger")
    cache.clear()
    referer = request.headers["Referer"]
    return redirect(referer)