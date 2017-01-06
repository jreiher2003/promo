from app import app, db, mail
from flask import Blueprint, render_template
from flask_mail import Message


promo_blueprint = Blueprint("promo", __name__, template_folder="templates")

@promo_blueprint.route("/testmail")
def testmail():

    msg = Message("Hello", recipients=["jeffreiher@gmail.com"])
    msg.body = "testing"
    msg.html = "<b>Testing</b>"
    mail.send(msg)
    return "sent"

@promo_blueprint.route("/tos")
def tos():
    return render_template("termsofservice.html")

@promo_blueprint.route("/private-policy")
def private_policy():
    return render_template("privacypolicy.html")