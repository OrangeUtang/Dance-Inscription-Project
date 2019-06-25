import secrets
import os
from flask import render_template, url_for, flash, redirect, request
from Languini import app, db, bcrypt
from Languini.models import Movement, Link, AnswersSet, Strain


@app.route("/")
@app.route("/home")
def home():
    return render_template('Home.html')


@app.route("/Study")
def study():
    #TODO
    print()


@app.route("/TestForm")
def test_form():
    #TODO
    print()


def submit():
    #TODO
    print()

