import os
from flask import Flask, flash, render_template, redirect, jsonify, request, g, session
from flask_debugtoolbar import DebugToolbarExtension
import requests
from newsapi import NewsApiClient

from sqlalchemy.exc import IntegrityError

from models import db, connect_db, News, User, Category, Save
from forms import UserForm, LoginForm, UserEditForm
from keys import API_KEY

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///news_app'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a top secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

CURR_USER_KEY = "curr_user"
newsapi = NewsApiClient(api_key=API_KEY)

##############################################################################
# User signup/login/logout/edit

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


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle login user"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            # flash(f"Hello, {user.username}!", "success")
            return redirect("/")
        else:
            flash(f"username or password is not valid", "danger")

    return render_template('login.html', form=form)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """sign up the user"""

    form = UserForm()

    if form.validate_on_submit():
        category = Category.retrieve_or_add(form.category.data)
        try:
            user = User.signup(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                category_id=category.id
            )
            db.session.commit()

        except IntegrityError:
            form.username.errors.append('Username already taken.')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)


@app.route('/logout')
def logout():
    """logout the user"""

    do_logout()
    flash('See you again!', 'info')
    return redirect('/login')

@app.route('/profile')
def user_info():
    """Show user's info"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect('/')

    return render_template('user.html')

@app.route('/edit', methods=["GET", "POST"])
def user_edit():
    """Edit a current user"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect('/')
    
    form = UserEditForm(obj=g.user, category=g.user.interest.name)

    if form.validate_on_submit():
        category = Category.retrieve_or_add(form.category.data)
        print(" ************************************************************ ")
        print(category.name)
        g.user.email = form.email.data
        g.user.category_id = category.id
        db.session.add(g.user)
        db.session.commit()
        flash('Successfully saved!', 'success')
        return redirect('/profile')

    return render_template('edit.html', form = form)
##############################################################################
# News request

@app.route('/')
def home():
    """show homepage"""
    # top_res = newsapi.get_top_headlines(country='us',
    #                                     language='en')
    # top_headlines = top_res['articles']

    # if g.user:
    #     user_cat = g.user.interest
    #     # print(" ******************************* g.user.interest ******************************* ")
    #     # print(user_cat.name)
    #     # print(" ******************************************************************************* ")
    #     interest_res = newsapi.get_top_headlines(country='us',
    #                                              category=user_cat.name,
    #                                              language='en')

    #     interest_news = interest_res['articles']
    #     return render_template('index.html', interest_news = interest_news, top_headlines=top_headlines)
    # else:
    #     return render_template('index.html', top_headlines=top_headlines)
    return render_template('base.html')
