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


db = SQL("sqlite:///autowood.db")


def countdays():

    prod_status  = db.execute("SELECT P,T,N,S,O,EAN_CODE FROM production;")
    status = []
    for i in range(len(prod_status)):
        for data in prod_status:
           suma = 0
           for key, value in prod_status[i].items():
            if key != "EAN_CODE":
                suma += value
           data = {prod_status[i]['EAN_CODE']:suma}
        status.append(data)
    return status

 
