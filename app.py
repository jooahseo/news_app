import os
from flask import Flask, flash, render_template, redirect, jsonify, request, g, session
from flask_debugtoolbar import DebugToolbarExtension
import requests

from sqlalchemy.exc import IntegrityError

from models import db, connect_db, News, User
from forms import UserForm, LoginForm
from keys import API_KEY

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///news'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a top secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

CURR_USER_KEY = "curr_user"
##############################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user to session"""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user from session"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/')
def home():
    """show homepage"""
    return render_template('index.html')

@app.route('/login', methods=["GET","POST"])
def login():
    """Handle login user"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")
    
    return render_template('login.html', form=form)


@app.route('/signup', methods=["GET","POST"])
def signup():
    """sign up the user"""

    form = UserForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                category=form.category.data 
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)


@app.route('/logout')
def logout():
    """logout the user"""
