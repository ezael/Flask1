from flask import Flask, render_template, request, session, redirect, url_for
from lib import db

app = Flask(__name__)
app.secret_key = "7u`u3rKq'{AW`3P"

user = {
    "username": "",
    "email": "",
    "lang": "fr",
    "id": 0
}

testDict = {
    "tt1": {
        "ema1": "rrrrr",
        "ema2": "ttttt"
    },
    "tt2": {
        "ema1": "oooooo",
        "ema2": "gdfgdgfd"
    }
}

@app.route('/')
def index():
    if "email" not in session:
        return redirect(url_for("login"))

    return redirect(url_for("game"))


@app.route("/login", methods=['GET', 'POST'])
def login():
    context = {
        "user_exist": 0
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

    return redirect(url_for("login"))


@app.route("/new_account", methods=['GET', 'POST'])
def new_account():
    context = {
        "user_exist": 0
    }

    if request.method == "POST":
        form_username = request.form['username']
        form_email = request.form['email'
        form_lang = request.form['lang']

        if form_username != "" and form_email != "":
            user_exist = db.user_exist(form_username, form_email)

            if not user_exist:
                if form_username != "" and form_email != "":
                    result = db.user_save(form_username, form_email, form_lang)

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

    if user['username'] != session['username']:
        return redirect(url_for("login"))

    if user['email'] != session['email']:
        return redirect(url_for("login"))

    context = {
        "user": user,
        "testDict": testDict
    }

    return render_template("game.html", ctx=context)

