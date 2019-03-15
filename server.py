from flask import Flask, render_template, request, session, redirect, url_for
from lib import db
from data import *
from trad import *

app = Flask(__name__)
app.secret_key = "7u`u3rKq'{AW`3P"

user = {
    "username": "",
    "email": "",
    "lang": "fr",
    "id": 0
}


@app.route('/')
def index():
    if "email" not in session:
        return redirect(url_for("login"))

    return redirect(url_for("game"))


@app.route("/login", methods=['GET', 'POST'])
def login():
    context = {
        "user_exist": 0,
        "trad": trad['fr']
    }
    if request.method == "POST":
        form_username = request.form['username']
        form_email = request.form['email']

        user_exist = db.user_exist(form_username, form_email)

        if not user_exist:
            context['user_exist'] = 2
        else:
            x = db.user_get(form_username, form_email)

            user['lang'] = x[3]
            user['id'] = x[0]
            user['username'] = form_username
            user['email'] = form_email

            session['username'] = form_username
            session['email'] = form_email
            session['lang'] = user['lang']
            session['id'] = user['id']

            return redirect(url_for("game"))

    return render_template("login.html", ctx=context)


@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("email", None)
    session.pop("lang", None)
    session.pop("id", None)

    return redirect(url_for("login"))


@app.route("/new_account", methods=['GET', 'POST'])
def new_account():
    context = {
        "user_exist": 0,
        "trad": trad['fr']
    }

    if request.method == "POST":
        form_username = request.form['username']
        form_email = request.form['email']
        form_lang = request.form['lang']

        if form_username != "" and form_email != "":
            user_exist = db.user_exist(form_username, form_email)

            if not user_exist:
                result = db.user_save(form_username, form_email, form_lang)

                user['lang'] = form_lang
                user['id'] = result
                user['username'] = form_username
                user['email'] = form_email

                session['username'] = form_username
                session['email'] = form_email
                session['lang'] = user['lang']
                session['id'] = result

                return redirect(url_for("game"))
            else:
                context['user_exist'] = 2

    return render_template("new_account.html", ctx=context)


@app.route("/game")
def game():
    # ----- security checks -----
    if "username" not in session:
        return redirect(url_for("login"))

    if "email" not in session:
        return redirect(url_for("login"))

    if user['username'] != session['username'] or user['email'] != session['email']:
        return redirect(url_for("login"))

    context = {
        "user": user,
        "trad": trad[user['lang']],
        "construction": construction[user['lang']]
    }

    return render_template("game.html", ctx=context)
