import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import uuid
import cv2
import shutil

import pandas as pd
from sqlalchemy import create_engine
from cs50 import SQL
from pdf2image import convert_from_path
from glob import glob
from pyzbar import pyzbar
from flask import redirect, render_template, session
from functools import wraps

db = SQL("sqlite:///autowood.db")


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def decode(image):
    orders = []
    decoded_objects = pyzbar.decode(image)
    for obj in decoded_objects:
        data = obj.data
        order = int(data.decode()[0:])
        orders.append(order)
    return image, orders


def impdb():
    df = pd.read_excel('sekwojaean.xls')
    engine = create_engine('sqlite:///autowood.db')
    df.to_sql('stockroom', con=engine)



#def pdfconvert():
    pages = convert_from_path("/pdforders/barcode*.png", 200)
    i = 0
    for page in pages(0, i):
        page.save(f"barcode{i}.png", "PNG")

def move_file(filename):

    src = f'orders/{filename}'
    dst = f'orders/archived_orders/{filename}'
    shutil.move(src,dst)
