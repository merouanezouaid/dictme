import os
import requests
import urllib.parse
import json
import psycopg2
import redis

from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from checkers import login_required, errorCheck

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
#app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_REDIS"] =  os.getenv('__REDIS URL (sensitive information)__')

Session(app)

# Configure psycopg2 to use postgreSQL database

conn = psycopg2.connect("__link to postgres database (sensitive information)__")

db = conn.cursor()


# the routes

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/search")
@login_required
def search():
    # close communication with the database
    return render_template("search.html")


@app.route("/word", methods=["GET", "POST"])
@login_required
def word():
    word = request.args.get('word')
    lang = request.args.get('language')

    # error checking for symbol

    if not word or not lang:
        flash('something is missing, try again!')
        return redirect("/search")

    wordDictionary = errorCheck(word)

    if not wordDictionary:
        return render_template("nomatch.html", word=word)

    user_id = session["user_id"]

    phonetic = wordDictionary["phonetic"]
    origin = wordDictionary["origin"]
    definition = wordDictionary["definition"]
    audio = wordDictionary["audio"]

    db.execute("INSERT INTO words (user_id, name, language) VALUES (%s, %s, %s)", (user_id, word, lang))

    # commit the changes to the database
    # commit the changes to the database
    conn.commit()
    # close communication with the database
    return render_template("word.html", phonetic=phonetic, origin=origin, definition=definition, audio=audio, word=word)


@app.route("/history")
@login_required
def history():
    """Show history of words searched"""

    user_id = session["user_id"]
    db.execute("SELECT name, language, date FROM words WHERE user_id = %s", [user_id])
    searched = db.fetchall()
    # commit the changes to the database
    # commit the changes to the database
    conn.commit()

 #   for i in searched:
 #      print(i.name)
    # close communication with the database
    return render_template("history.html", searched=searched)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash('Must provide username')
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('Must provide password')
            return render_template("login.html")

        # Query database for username

        db.execute("SELECT * FROM users WHERE username = %s", (request.form.get("username"),))
        rows = db.fetchall()
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            flash('invalid username and/or password')
            return render_template("login.html")

        # Remember which user has logged in
        flash('You were successfully logged in')

        session["user_id"] = rows[0][0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        # Redirect user to home page
        return redirect("/search")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    flash('You were successfully logged out')

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            flash('Username is missing')
            return render_template("register.html")
        elif not password:
            flash('Password is missing')
            return render_template("register.html")
        elif not confirmation:
            flash('Must confirm your password')
            return render_template("register.html")

        if password != confirmation:
            flash('Passwords don\'t match')
            return render_template("register.html")

        # checks if the username is already used
        db.execute("SELECT username from users WHERE username = %s", [username])
        usercheck = db.fetchall()

        if (len(usercheck) > 0):
            flash('Username is already used.. Try a different one!')
            return render_template("register.html")

        token = generate_password_hash(password)
        db.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, token))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        flash('You have been registered successfully!!')
        return render_template("login.html")

    else:
        return render_template("register.html")


@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    """Change password"""
    if request.method == "POST":
        user_id = session["user_id"]
        newpassword = request.form.get("new")
        confirmation = request.form.get("confirmation")

        if not newpassword:
            flash('New Password is missing!')
            return render_template("changepassword.html")
        elif not confirmation:
            flash('Must confirm your password.')
            return render_template("changepassword.html")

        if newpassword != confirmation:
            flash('Passwords don\'t match.')
            return render_template("changepassword.html")

        newtoken = generate_password_hash(newpassword)
        db.execute("UPDATE users SET password = %s WHERE user_id = %s", (newtoken, user_id))

        # commit the changes to the database
        conn.commit()
        # close communication with the database
        flash('Your password has been changed successfully!')

        return render_template("login.html")

    else:
        return render_template("changepassword.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return error(e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


def error(e):
    return render_template("error.html", e=e)

