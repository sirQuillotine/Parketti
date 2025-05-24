import sqlite3
from flask import Flask
from flask import redirect, render_template, abort, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import event

app = Flask(__name__)
app.secret_key = "ananas"


@app.route("/")
def index():
    query = request.args.get("query")
    if query:
        events = event.search_events(query)
    else:
        events = event.get_events()
    return render_template("index.html", query=query, events=events, session=session)

@app.route("/register")
def register():
    return render_template("register.html")


    
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        start_time = request.form["start_time"]
        styles = request.form.getlist("styles")
        event_id = event.add_event(title, content, start_time, session["username"], styles)
        return redirect("/")


@app.route("/event/<int:event_id>", methods=["GET", "POST"])
def event_details(event_id):
    show_participation = True
    event_e = event.get_event(event_id)
    event_styles = event.get_event_styles(event_id)
    event_participants = event.get_event_participants(event_id)

    if request.method == "POST":
        if session["username"] in event_participants:
            print("poistetaan osallistuja")
            event.delete_participant(event_id, session["username"])
        else:
            print("lisätään osallistuja")
            event.add_participants(event_id, session["username"])
        event_participants = event.get_event_participants(event_id)

    if "username" in session.keys():
        if session["username"] in event_participants:
            show_participation = False
    return render_template("event.html", event=event_e, styles=event_styles, participants=event_participants, show=show_participation, session=session)



@app.route("/edit/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    event_e = event.get_event(event_id)
    if event_e["username"] != session["username"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit.html", event=event_e)
    
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        start_time = request.form["start_time"]
        event.update_event(event_id, title, content, start_time)
        return redirect("/")

@app.route("/delete/<int:event_id>", methods=["GET", "POST"])
def delete_event(event_id):
    event_r = event.get_event(event_id)
    if event_r["username"] != session["username"]:
        abort(403)

    if request.method == "GET":
        return render_template("delete.html", event=event_r)

    if request.method == "POST":
        if "continue" in request.form:
            event.delete_event(event_r["id"])
        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        sql = "SELECT password_hash FROM users WHERE username = ?"
        password_hash = db.query(sql, [username])[0][0]

        if check_password_hash(password_hash, password):
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

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
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return redirect("/")