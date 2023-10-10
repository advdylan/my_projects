import os
import pandas as pd
import cv2


from glob import glob
from pyzbar import pyzbar
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, Response
from flask import *
from flask_session import Session
from fileinput import filename
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date


from helpers import login_required, apology, decode, impdb

UPLOAD_FOLDER = os.path.join('csvfiles')

ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.secret_key = '2162445'

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

    eans = []
    barcodes = glob("orders/barcode*.png")
    for barcode_file in barcodes:
        img = cv2.imread(barcode_file)
        img, orders = decode(img)
        order = orders[0]
        cv2.waitKey(0)
    
        eans_request = db.execute('SELECT * FROM sekwojaean WHERE "Kod EAN" = ?', order )
        eans.append(eans_request[0])
    
        
    return render_template("eanreader.html", eans=eans)


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


#@app.route("/orders")
#def showData():

@app.route("/production", methods=["GET", "POST"])
@login_required
def production():

    week_list = db.execute("SELECT DISTINCT week FROM orders")

    if request.method == "GET":
        return render_template("production.html", week_list = week_list)
    
    
@app.route("/productiontable", methods = ["GET", "POST"])
@login_required
def productiontable():

    #Masz błąd w wyświetlaniu tej tabeli. Używasz tabeli order w której nie ma PTNSO
    if request.method == "GET":
        return render_template("productiontable.html")
    if request.method == "POST":
        production_week = request.form.get("show")
        orders = db.execute('SELECT * FROM production JOIN sekwojaean ON production.EAN_CODE = sekwojaean."Kod EAN" WHERE week = ?', production_week)
        return render_template("productiontable.html", orders = orders)
    
@app.route("/submit_changes", methods=["POST"])
@login_required
def update_table():
    if request.method == "POST":
        production_week = request.form.get("production_week")
        print(production_week)
        # Get the values of the checked checkboxes
        p = request.form.get('P')
        # Update the values in the database
        orders = db.execute('SELECT * FROM production JOIN sekwojaean ON production.EAN_CODE = sekwojaean."Kod EAN" WHERE week = ?', production_week)
        return render_template("productiontable.html", orders = orders)
        

@app.route("/insertorder", methods=["GET", "POST"])
@login_required
def insertorder():
        
    eans = db.execute('SELECT "Kod EAN" FROM sekwojaean;')
    if request.method == "POST":
        if request.form['submit_button'] == 'insert':
            eanchosen = request.form.get("eanchosen")
            current_date = date.today()
            week = request.form.get("week")
            week = int(week)
            if week == 0 or week >= 52:
                flash("Wrong week number", "danger")
                return redirect("/insertorder")
            zd = request.form.get("ZD")
            if zd == '0':
                flash("Wrong ZD number", "danger")
                return redirect("/insertorder")
            flash("Succes", "success" )
            db.execute("INSERT INTO orders (EAN_CODE, date, week, zd) VALUES (?, ?, ?, ?)", eanchosen, current_date, week, zd)
            return render_template("insertorder.html")
            
        
        elif request.form['submit_button'] == 'check':
            eancheck = request.form.get("eanchosen")
            eanviewer = db.execute('SELECT * FROM sekwojaean WHERE "Kod Ean" = (?)', eancheck)
            return render_template("insertorder.html", eans = eans, eancheck = eancheck, eanviewer = eanviewer)
    
    if request.method == "GET":
        return render_template("insertorder.html", eans=eans)
    

@app.route("/ordersweek", methods=["GET", "POST"])
@login_required
def ordersweek():

    week_list = db.execute("SELECT DISTINCT week FROM orders")

    if request.method == "GET":
        return render_template("ordersweek.html", week_list = week_list)
    
    
@app.route("/orders", methods=["GET", "POST"])
@login_required
def orders():

    orders = db.execute('SELECT * FROM orders JOIN sekwojaean ON orders.EAN_CODE = sekwojaean."Kod EAN"')

    if request.method == "GET":
        return render_template("orders.html")
    if request.method == "POST":
        production_week = request.form.get("showorder")
        orders = db.execute('SELECT * FROM orders JOIN sekwojaean ON orders.EAN_CODE = sekwojaean."Kod EAN" WHERE week = ?', production_week)
        return render_template("orders.html", orders = orders)


@app.route("/update_checkbox", methods = ["POST"])
@login_required
def update_checkbox():
    checkbox_id = request.form.get('id')
    checkbox_status = request.form.get('status')
    checkbox_name = request.form.get('name')
    db.execute('UPDATE production SET ? = ? WHERE id = ?', checkbox_name, checkbox_status, checkbox_id)
    

@app.route("/delete_row", methods =["POST"])
@login_required
def delete_row():

    if request.method == "POST":
        row_id = request.form.get("indexcode")
        db.execute("DELETE FROM ORDERS WHERE EAN_CODE = ?", row_id)
        return redirect("/orders")
    
@app.route("/delete_wrow", methods =["POST"])
@login_required
def delete_wrow():

    if request.method == "POST":
        row_id = request.form.get("indexcode")
        db.execute("DELETE FROM warehouse WHERE EAN_CODE = ?", row_id)
        return redirect("/warehouse")
    
@app.route("/sendtoproduction", methods =["POST"])
@login_required
def sendtoproduction():
    if request.method == "POST":
        row_id = request.form.get("indexcode") 
        print(row_id)
        zd = request.form.get("ZD")
        current_date = date.today()
        print(zd)
        week = request.form.get("week")
        print(week)
        flash("Success", "success")
        db.execute("INSERT INTO production (EAN_CODE, date, week, ZD, P, T, N, S, O) VALUES (?, ?, ?, ?, 0, 0, 0, 0, 0)", row_id, current_date, week, zd)
        return jsonify({"message": "Success"}), 200

@app.route("/insert", methods=["GET", "POST"])
@login_required
def insert():     

    eans = db.execute('SELECT "Kod EAN" FROM sekwojaean;')
    if request.method == "POST":
        if request.form['submit_button'] == 'insert':
            eanchosen = request.form.get("eanchosen")
            db.execute("INSERT INTO warehouse (EAN_CODE) VALUES (?)", eanchosen)

            return redirect("/warehouse")
        elif request.form['submit_button'] == 'check':
            eancheck = request.form.get("eanchosen")
            eanviewer = db.execute('SELECT * FROM sekwojaean WHERE "Kod Ean" = (?)', eancheck)
            return render_template("insert.html", eans = eans, eancheck = eancheck, eanviewer = eanviewer)
    
    if request.method == "GET":
        return render_template("insert.html", eans=eans)

    

@app.route("/warehouse", methods=["GET", "POST"])
@login_required
def warehouse():

    warehouse = db.execute('SELECT * FROM warehouse JOIN sekwojaean ON warehouse.EAN_CODE = sekwojaean."Kod EAN"')
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
