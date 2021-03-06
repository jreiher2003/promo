import urllib2 # pragma: no cover
import requests # pragma: no cover
import json # pragma: no cover
import logging
from app import app, db, cache, bcrypt # pragma: no cover
from flask import render_template, request, url_for, redirect, flash, abort, Blueprint # pragma: no cover
from flask_login import current_user, login_required

from app.users.models import Users
from app.ascii.models import AsciiArt # pragma: no cover
from app.ascii.forms import AsciiForm # pragma: no cover

ascii_blueprint = Blueprint("ascii", __name__, template_folder="templates")

def get_ip():
    headers_list = request.headers.getlist("X-Forwarded-For")
    user_ip = headers_list[0] if headers_list else request.remote_addr
    return user_ip

IP_URL = "http://ip-api.com/json/"
def get_coords(ip):
    ip = get_ip()
    try:
        url = IP_URL + ip
    except TypeError:
        url = IP_URL + "73.55.103.114"
    content = None
    try:
        content = urllib2.urlopen(url).read()
    except URLError:
        return
    if content:
        try:
            result = json.loads(content)
            lat = float(result["lat"])
            lon = float(result["lon"])
            return (lat,lon)
        except KeyError:
            lat = "50.00"
            lon = "50.00"
            return (lat,lon)
    else:
        return None

def gmaps_img(points):
    GMAPS_URL = "https://maps.googleapis.com/maps/api/staticmap?size=550x400&zoom=3&sensor=false&key=AIzaSyDOnmHKt4bMXj-QL8pKeHd4yCyTL8-IzUc"
    for lat, lon in points:
        GMAPS_URL += '&markers=%s,%s' % (lat, lon)
    return GMAPS_URL

def top_arts(update=False):
    key = "top"
    all_art = cache.get(key)
    if all_art is None or update:
        logging.error("DB QUERY")
        all_art = AsciiArt.query.order_by(AsciiArt.id.desc()).all()
        all_art = list(all_art)
        cache.set(key, all_art)
    return all_art

def top_users(update=False):
    key = "all_uses"
    all_users = cache.get(key)
    if all_users is None or update:
        logging.error("Users DB QUERY")
        all_users = Users.query.all()
        all_users = list(all_users)
        cache.set(key, all_users)
    return all_users 

@ascii_blueprint.route("/ascii", methods=["GET","POST"])
@login_required
def hello():
    all_art = top_arts()
    all_users = top_users()
    form = AsciiForm()
    ip = get_ip()
    error = None
    lat = [a.lat for a in all_art]
    lon = [b.lon for b in all_art]
    gps = zip(lat,lon)
    img_url = None
    img_url = gmaps_img(gps)
    if form.validate_on_submit():
        one = AsciiArt(title=form.title.data, art=form.art.data, user_id=current_user.id)
        lat = get_coords(ip)[0]
        lon = get_coords(ip)[1]
        if lat and lon:
            one.lat = lat
            one.lon = lon
        db.session.add(one)
        db.session.commit()
        top_arts(True)
        top_users(True)
        flash("You just posted some <strong>ascii</strong> artwork!", "success")
        return redirect(url_for("hello"))
    return render_template("front.html", 
        all_art=all_art,
        all_users=all_users, 
        img_url=img_url, 
        form=form, 
        error=error)

@ascii_blueprint.route("/<int:art_id>/edit", methods=["GET","POST"])
@login_required
def edit_art(art_id):
    all_art = top_arts()
    all_users = top_users()
    lat = [a.lat for a in all_art]
    lon = [b.lon for b in all_art]
    gps = zip(lat,lon)
    img_url = None
    img_url = gmaps_img(gps)
    error = None
    edit_art = AsciiArt.query.filter_by(id=art_id).one()
    form = AsciiForm(obj=edit_art)
    if form.validate_on_submit():
        edit_art.title = form.title.data
        edit_art.art = form.art.data
        db.session.add(edit_art)
        db.session.commit()
        top_arts(True)
        top_users(True)
        flash("Successful Edit of <strong>%s</strong>" % edit_art.title, "info")
        return redirect(url_for("hello"))
    return render_template("edit.html", 
        error=error, 
        edit_art=edit_art, 
        form=form, 
        all_art=all_art,
        all_users=all_users, 
        img_url=img_url)

@ascii_blueprint.route("/<int:art_id>/delete", methods=["GET","POST"])
@login_required
def delete_art(art_id):
    delete_artwork = AsciiArt.query.filter_by(id=art_id).one()
    form = AsciiForm()
    if request.method == "POST":
        db.session.delete(delete_artwork)
        db.session.commit()
        top_arts(True)
        top_users(True)
        flash("Just deleted <u>%s</u>" % delete_artwork.title, "danger")
        return redirect(url_for("hello"))
    return render_template("delete.html", 
        delete_artwork=delete_artwork)

@ascii_blueprint.route("/ajax", methods=["GET","POST"])
@login_required
def ajax():    
    return render_template("ajax.html")

@ascii_blueprint.route("/puppy-api-example", methods=["GET", "POST"])
@login_required
def pup_api():
    url = "http://adopt-puppy.herokuapp.com/shelters/.json"
    response = requests.get(url)
    shelters = response.json()
    return render_template("pup-api.html", shelters=shelters)

