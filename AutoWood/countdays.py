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

    keys = ['ean', 'empty', 'done']
    order = dict.fromkeys(keys)
    done = 0
    fails = 0
    for d in prod_status:
        for value in d.values():
            if value == 0:
                fails += 1
            elif value == 1:
                done += 1
        order['ean'] = d['EAN_CODE']
        order['empty'] = fails
        order['done'] = done

    print(f"Fails: {fails}, done: {done}")
    print(order)
        



countdays()