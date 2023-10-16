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
    #print(prod_status)
    empty = []
    done = []
    for EAN_CODE in prod_status:
        EAN_ID = []
        EAN_ID.append["EAN_CODE"]
        print(EAN_CODE["EAN_CODE"])
        



countdays()