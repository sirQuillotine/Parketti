import sqlite3
import secrets
from datetime import datetime
import math
import time

from flask import Flask
from flask import redirect, render_template, abort, request, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
import markupsafe


import db
import event



app = Flask(__name__)
app.secret_key = "ananas"

@app.template_filter()
def format_datetime(start_time):
    date = datetime.strptime(start_time, "%Y-%m-%d")
    return date.strftime("%d.%m.%Y")

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_size = 20
    event_count = event.get_event_count()
    page_count = math.ceil(event_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))
    
    query = request.args.get("query")
    if query:
        events = event.search_events(query, page, page_size)
    else:
        events = event.get_events(page, page_size)
    return render_template("index.html", query=query, events=events, page=page,
                            page_count=page_count, session=session)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/add", methods=["GET", "POST"])
def add():
    if not "username" in session.keys():
        abort(403)
    if request.method == "GET":
        styles = event.get_styles()
        return render_template("add.html", session=session, styles=styles)

    if request.method == "POST":
        check_csrf()

        title = request.form["title"]
        if not title or len(title) > 100:
            abort(403)
        content = request.form["content"]
        if not content or len(content) > 1000:
            abort(403)
        start_time = request.form["start_time"]
        if not start_time:
            abort(403)
        try:    
            datetime.strptime(start_time, "%Y-%m-%d")
        except ValueError:
            abort(403)
        styles = request.form.getlist("styles")
        event.add_event(title, content, start_time, session["username"], styles)
        return redirect("/")


@app.route("/event/<int:event_id>", methods=["GET", "POST"])
def event_details(event_id):
    show_participation = True
    event_e = event.get_event(event_id)
    event_styles = event.get_event_styles(event_id)
    event_participants = event.get_event_participants(event_id)

    if request.method == "POST":
        check_csrf()
        if session["username"] in event_participants:
            event.delete_participant(event_id, session["username"])
        else:
            event.add_participants(event_id, session["username"])
        event_participants = event.get_event_participants(event_id)

    if "username" in session.keys():
        if session["username"] in event_participants:
            show_participation = False
    return render_template("event.html", event=event_e, styles=event_styles,
                            participants=event_participants, show=show_participation,
                            session=session)

@app.route("/user/<username>/")
def user(username):
    page1 = request.args.get("own")
    page2 = request.args.get("part")

    if not page1:
        page1 = 1
    if not page2:
        page2 = 1

    try:
        page1 = int(page1)
        page2 = int(page2)
    except:
        page1 = 1
        page2 = 1

    page_size = 5

    event_count = event.get_user_event_count(username)
    page1_count = math.ceil(event_count / page_size)
    page1_count = max(page1_count, 1)

    participation_count = event.get_user_participation_count(username)
    page2_count = math.ceil(participation_count / page_size)
    page2_count = max(page2_count, 1)

    if page1 < 1 or page1 > page1_count or page2 < 1 or page2 > page2_count:
        return redirect("/user/" + username + "?own=1")

    events = event.get_user_events(username, page1, page_size)
    participations = event.get_user_participations(username, page2, page_size)
    return render_template("user.html", events=events, event_count=event_count,
                            page1=page1,
                            page1_count=page1_count,
                            participations=participations, participation_count=participation_count,
                            page2=page2, page2_count=page2_count,
                            username=username)



@app.route("/edit/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    event_e = event.get_event(event_id)
    if event_e["username"] != session["username"]:
        abort(403)

    if request.method == "GET":
        styles = event.get_styles()
        return render_template("edit.html", event=event_e, session=session, next_page=request.referrer, styles=styles)

    if request.method == "POST":
        check_csrf()
        title = request.form["title"]
        if not title or len(title) > 100:
            abort(403)
        content = request.form["content"]
        if not content or len(content) > 1000:
            abort(403)
        start_time = request.form["start_time"]
        if not start_time:
            abort(403)
        try:    
            datetime.strptime(start_time, "%Y-%m-%d")
        except ValueError:
            abort(403)
        event_styles = request.form.getlist("styles")
        next_page = request.form["next_page"]
        event.update_event(event_id, title, content, start_time, styles=event_styles)
        return redirect(next_page)

@app.route("/delete/<int:event_id>", methods=["GET", "POST"])
def delete_event(event_id):
    event_r = event.get_event(event_id)
    if event_r["username"] != session["username"]:
        abort(403)

    if request.method == "GET":
        return render_template("delete.html", event=event_r, session=session, next_page=request.referrer)

    if request.method == "POST":
        
        check_csrf()
        if "continue" in request.form:
            event.delete_event(event_r["id"])
        next_page = request.form["next_page"]
        return redirect(next_page)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT password_hash FROM users WHERE username = ?"
        password_hash = db.query(sql, [username])[0][0]
        if not check_password_hash(password_hash, password):
            return "VIRHE: väärä tunnus tai salasana"
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register")
    password_hash = generate_password_hash(password1)

    if not username.isalpha():
        flash("VIRHE: käyttäjätunnus saa sisältää vain kirjaimia")
        return redirect("/register")
    if len(username) < 3 or len(username) > 20:
        flash("VIRHE: käyttäjätunnuksen tulee olla 3-20 merkkiä pitkä")
        return redirect("/register")
    if len(password1) < 3:
        flash("VIRHE: salasanan tulee olla vähintään 3 merkkiä pitkä")
        return redirect("/register")
    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")
    flash("Käyttäjä luotu onnistuneesti")
    return redirect("/register")


def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response
