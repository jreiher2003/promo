from app import app, db, mail
from flask import Blueprint
from flask_mail import Message


promo_blueprint = Blueprint("promo", __name__, template_folder="templates")

@promo_blueprint.route("/testmail")
def testmail():

    msg = Message("Hello", recipients=["jeffreiher@gmail.com"])
    msg.body = "testing"
    msg.html = "<b>Testing</b>"
    mail.send(msg)
    return "sent"