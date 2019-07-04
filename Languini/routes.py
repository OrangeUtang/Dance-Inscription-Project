import secrets
import os
from flask import render_template, url_for, flash, redirect, request, jsonify, make_response
from Languini import app, db, bcrypt
from Languini.forms import LoginForm
from Languini.models import Movement, Answer, Link, Strain, Admin, MoveList
from flask_login import login_user, current_user, logout_user, login_required

@app.errorhandler(404)
def page_not_found(e):
    code = 404
    msg = "404: Not Found"
    return render_template('Error.html', title=str(code), msg=msg)


@app.route("/")
@app.route("/Home")
def home():
    return render_template('Home.html', title="Home")


@app.route("/Study")
def study():
    #TODO
    print()


@app.route("/Test")
def test_form():
    #TODO
    print()


def submit():
    #TODO
    print()


@app.route("/Admin", methods={"GET"})
def display_loggin():
    form = LoginForm()
    return render_template('Login.html', title="Login", form=form)


@app.route("/Admin", methods={"POST"})
def login():
    form = LoginForm()
    # check if credential are valid
    if form.validate_on_submit():
        user = Admin.quety.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/Admin/AddVid", methods={"POST"})
def uploadVidList():
    """
    upload a list of vid url and associated ref number to the database
    take in a string (or file) containing a list of
    """
    vid_list = request.form.get("vidList")


#Function to set initial User up
def Factory_setup():
    """
    Set admin to defaut values
    reset database to default values
    """
    print()
