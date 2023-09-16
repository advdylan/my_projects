import os
import pandas as pd
import cv2


from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask import *
from flask_session import Session
from fileinput import filename
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date


from helpers import login_required, apology

UPLOAD_FOLDER = os.path.join('csvfiles')

ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

db = SQL("sqlite:///autowood.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/eanreader", methods=["GET", "POST"])
@login_required
def eanreader():
    return render_template("warehouse.html")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    return render_template("index.html")

@app.route('/uploader')
def upload_file():
   return render_template('uploader.html')

@app.route("/upload", methods=["GET", "POST"])
@login_required
def uploader():
    if request.method == "POST":
        f = request.files['file']
        data_filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],
                            data_filename))

        session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'],
                     data_filename)

        return redirect("/show_data")
    return redirect("/show_data")


@app.route("/show_data")
def showData():
    data_file_path = session.get('uploaded_data_file_path', None)
    uploaded_df = pd.read_csv(data_file_path, encoding = 'unicode_escape')

    uploaded_df_html = uploaded_df.to_html()
    return render_template('show_csv_data.html', data_var=uploaded_df_html)





@app.route("/insert", methods=["GET", "POST"])
@login_required
def insert():
    if request.method == "POST":
        EAN = request.form.get("EAN")
        type = request.form.get("type")
        model = request.form.get("model")
        color = request.form.get("color")
        wood = request.form.get("wood")
        size = request.form.get("size")

        db.execute("INSERT INTO furnitures (EAN,type,model,color,wood,size) VALUES (?, ?, ?, ?, ?, ?)",
                   EAN, type, model, color, wood, size)

        return render_template("warehouse.html", EAN = EAN, type = type, model=model,color=color, wood=wood,size=size)

    return render_template("insert.html")

@app.route("/warehouse", methods=["GET", "POST"])
def warehouse():

    warehouse = db.execute("SELECT * FROM FURNITURES")
    print(warehouse)

    return render_template("warehouse.html", warehouse=warehouse)

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session['username'] = rows[0]['username']

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # username
        name = request.form.get("username")
        # password
        password = request.form.get("password")
        # confirmation the password
        password2 = request.form.get("confirmation")

        if password != password2 or not password:
            # if passwords dont match
            return apology("passwords doesnt match", 400)

        if not name:
            # wrong name
            return apology("wrong username", 400)

        # hash the password
        password_hash = generate_password_hash(password)
        query = db.execute("SELECT * from USERS WHERE username=?", name)
        if len(query) == 0:
            db.execute("INSERT INTO users(username, hash) VALUES (?, ?);", name, password_hash)
            return render_template("register.html")
        else:
            return apology("username already exists", 400)

    return render_template("register.html")



