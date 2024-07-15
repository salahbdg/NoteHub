from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from notehub_helpers import login_required, generateSvg, transformString





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

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///noteHubDB.db")



@app.route("/")
def index():
    """Show the homepage"""

    # If user is not logged in, show the homepage
    if session.get("user_id") is None:
        return render_template("index.html")
    
    # If user is logged in, show the feed
    else:
      return render_template("feed.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        username = request.form.get("username").strip().upper()
        password = request.form.get("password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return render_template("login.html", error="Invalid username and/or password")
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")
    
    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # Get form data
        username = request.form.get("username").strip().upper()
        email = request.form.get("email").strip()
        password = request.form.get("password")
        confirmation_password = request.form.get("confirmation")

        # To check if the username is already taken
        users = db.execute("SELECT * FROM users WHERE username = ?", username)


        if (len(username) == 0) or (len(email) == 0) or (len(users) != 0) or (len(password.strip()) == 0) or (password != confirmation_password):
            return render_template("register.html", error="Invalid registration details. Please try again.")
        else:
            db.execute("INSERT INTO users (username,email, hash, favouriteID, noteID) VALUES (?,?,?,?,?)", username, email, generate_password_hash(password), 1, 1)
            return redirect("/login")

    return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/account")
@login_required
def account():
    """Show the account page"""

    return render_template("account.html")


@app.route("/blog")
def blog():
    """Show the blog page"""

    return render_template("blog.html")

# the associated function. 
@app.route("/discover", methods=["GET", "POST"])
def discover(): 
    
    if request.method == "GET":
      if session.get("user_id") is None:
        return redirect(url_for('login'))
      # username
      username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]

      # get language
      language = request.args.get('language')
      print(language)

      if language is None:
        return render_template("discover.html")
      
      else:

        chart, repos_dict = generateSvg(language, username)  # this will render output in flask app

        # this will render output in flask app
        return render_template('discover.html', chart = chart, repos_dict = repos_dict)
      
    #return render_template("discover.html")


