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



@app.route("/", methods=["GET", "POST"])
def index():
    """Show the homepage"""

    # If user is not logged in, show the homepage
    if session.get("user_id") is None:
        return render_template("index.html")
    
    # If user is logged in, show the feed
    else:
      """Show the feed page"""
      if request.method == "POST":
        # Get the post content
        title = request.form.get("title")
        post_content = request.form.get("postContent")

        # Insert the post into the database
        query = "INSERT INTO Posts (title, postText, userID) VALUES (?, ?, ?)"
        db.execute(query, title, post_content, session["user_id"])

        # Redirect to the feed
        return redirect("/")
      
      # Get the posts from the database
      query = "SELECT * FROM Posts ORDER BY postDate DESC"
      posts = db.execute(query)
      return render_template("feed.html", posts=posts)
  



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        username = request.form.get("username").strip().upper()
        password = request.form.get("password")

        # Query database for username
        query = "SELECT * FROM Users WHERE username = ?"
        rows = db.execute(query, username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hashPass"], password):
            return render_template("login.html", error="Invalid username and/or password")
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["ID"]
        session["username"] = rows[0]["username"]

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
        query = "SELECT * FROM Users WHERE username = ?"
        Users = db.execute(query, username)


        if (len(username) == 0) or (len(email) == 0) or (len(Users) != 0) or (len(password.strip()) == 0) or (password != confirmation_password):
            return render_template("register.html", error="Invalid registration details. Please try again.")
        else:
            query = "INSERT INTO Users (username,mail, hashPass) VALUES (?,?,?)"
            db.execute(query, username, email, generate_password_hash(password))
            return redirect("/login")

    return render_template("register.html")


@app.route("/logout")
@login_required
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

    query = "SELECT * FROM Users WHERE ID = ?"
    user = db.execute(query, session["user_id"])[0]

    return render_template("account.html", user=user)


@app.route("/blog")
def blog():
    """Show the blog page"""

    return render_template("blog.html")

# the associated function. 
@app.route("/discover", methods=["GET"])
@login_required
def discover(): 
    
    if session.get("user_id") is None:
      return redirect(url_for('login'))
    # username
    query = "SELECT username FROM Users WHERE ID = ?"
    username = db.execute(query, session["user_id"])[0]["username"]

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


@app.route("/deletePost", methods=["POST"])
@login_required
def delete():
    """Delete a post"""
    if request.method == "POST":
      # Get the post ID
      post_id = request.form.get("postID")
      print("gezzzzzzzzzzzzz")
      print(post_id)

      # Delete the post from the database
      query = "DELETE FROM Posts WHERE postID = ?"
      db.execute(query, post_id)

      return redirect("/")


@app.template_filter('getUsername')
def getUsername(userID):
    return db.execute("SELECT * FROM Users WHERE ID = ?", userID)[0]["username"].capitalize()

