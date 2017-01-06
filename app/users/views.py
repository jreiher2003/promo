import datetime
from app import app, db, cache, bcrypt 
from flask import render_template, url_for, redirect, request, Blueprint, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.users.forms import LoginForm, RegistrationForm, RecoverPasswordForm, ChangePasswordTokenForm
from app.users.models import Users, UserRoles
from app.users.utils import get_ip, is_safe_url, generate_confirmation_token, confirm_token, \
send_email, password_reset_email, email_reset_notice

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
            flash("You just logged in as %s!" % user.email, "success")
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
            token = generate_confirmation_token(user.email)
            confirm_url = url_for('users.confirm_email_register', token=token, _external=True)
            html = render_template("email/welcome.html", confirm_url=confirm_url, user=user)
            subject = "Please confirm your email"
            send_email(user.email, subject, html)
            login_user(user)
            flash("You have just signup up congrats!", "success")
            next = request.args.get("next")
            if not is_safe_url(next):
                return flask.abort(400)
            return redirect(next or url_for("ascii.hello"))
        except:
            flash("That email already exists", "danger")
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

@users_blueprint.route('/confirm/<token>/')
@login_required
def confirm_email_register(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = Users.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_at = datetime.datetime.now()
        user_roles = UserRoles(user_id=user.id, role_id=1)
        db.session.add_all([user, user_roles])
        db.session.commit()
        cache.clear()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('ascii.hello'))

@users_blueprint.route("/forgot-password/", methods=["GET","POST"])
def forgot_password():
    form = RecoverPasswordForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data, confirmed=False).one_or_none()
        if user is not None:
            password_reset_email(user.email)
            flash("sent email to %s" % user.email, "warning")
            return redirect(url_for("users.login"))
        else:
            flash("this account is not confirmed", "danger")
            return redirect(url_for("users.login"))
    return render_template("forgot_password.html", form=form)

@users_blueprint.route("/password-reset/<token>/", methods=["GET","POST"])
def forgot_password_reset_token(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = Users.query.filter_by(email=email).one_or_none()
    form = ChangePasswordTokenForm()
    if request.method == "POST": 
        user.password = request.form["password"]
        db.session.add(user)
        db.session.commit()
        email_reset_notice(user.email)
        flash("Successful password updated!", "success")
        cache.clear()
        return redirect(url_for("users.login"))
    return render_template("forgot_password_change.html", form=form, token=token)