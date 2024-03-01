import os
import math
import csv
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mtgocoll.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    limit = 100
    current_page = request.args.get('page', default = 1, type=int)
    offset = (current_page - 1) * limit
    cards = db.execute("SELECT * FROM collection ORDER BY set_sym ASC LIMIT :limit OFFSET :offset", limit = limit, offset = offset)
    recs = db.execute("SELECT COUNT(*) FROM collection")
    total_recs = recs[0]["COUNT(*)"]
    total_pages = math.ceil(total_recs/limit)
    start_page = max(current_page - 3, 1)
    end_page = min(current_page + 3, total_pages)
    visible_pages = range(start_page, end_page + 1)
    return render_template("index.html", cards = cards, limit = limit, current_page = request.args.get('page', default = 1, type=int), total_pages = total_pages, visible_pages = visible_pages)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]



        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        username = request.form.get("username")
        if not username:
            return apology("Please provide a Username")
        registered_users = db.execute("SELECT username FROM users WHERE username = ?", request.form["username"])
        if registered_users:
            return apology("User name already taken")
        password = request.form.get("password")
        if not password:
            return apology("Please provide a Password")
        password_confirmation = request.form.get("confirmation")
        if not password_confirmation:
            return apology("Please provide a password_confirmation")
        if request.form["password"] != request.form["confirmation"]:
            return apology("Password does not match Password Confirmation")
        hashed_password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hashed_password)
        flash("You are Registerd")
        return render_template("login.html")

    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
