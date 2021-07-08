import os
from flask import Flask, flash, render_template, redirect, jsonify, request, g, session
from flask_debugtoolbar import DebugToolbarExtension
import requests
from newsapi import NewsApiClient

from sqlalchemy.exc import IntegrityError

from models import db, connect_db, News, User, Category, Save
from forms import UserForm, LoginForm, UserEditForm, NewsForm
from keys import API_KEY
from news_mapper import News_List

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
BASE_URL = "https://newsapi.org/v2/"
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
        g.user.email = form.email.data
        g.user.category_id = category.id
        db.session.add(g.user)
        db.session.commit()
        flash('Successfully saved!', 'success')
        return redirect('/profile')

    return render_template('edit.html', form=form)

##############################################################################
# News request


@app.route('/')
def home():
    """show homepage"""
    top_res = newsapi.get_top_headlines(country='us',
                                        language='en')
    top_headlines = News_List()
    top_headlines.news_mapper(top_res)

    if g.user:
        user_category = g.user.interest.name.lower()
        interest_res = newsapi.get_top_headlines(country='us',
                                                 category=user_category,
                                                 language='en')
        interest_news = News_List()
        interest_news.news_mapper(interest_res)

        return render_template('index.html', interest_news=interest_news.list, top_headlines=top_headlines.list)
    else:
        return render_template('index.html', top_headlines=top_headlines.list)


@app.route('/news')
def news_list():
    """page with listing of news that a user searches for"""

    search = request.args.get('q')
    print(" *************************** I SEARCHED ********************************* ")
    print(search)
    if not search:
        all_res = newsapi.get_top_headlines(country='us', language='en')
        all_articles = News_List()
        all_articles.news_mapper(all_res)

        return render_template('search.html', articles=all_articles.list)
    else:
        # res = requests.get(f"{BASE_URL}everything?qInTitle={search}&language=en&sortBy=popularity&apiKey={API_KEY}")
        res = newsapi.get_everything(q=search,
                                     language='en',
                                     sort_by='publishedAt')

        articles = News_List()
        articles.news_mapper(res)

        return render_template('search.html', articles=articles.list, q=search)

@app.route('/save-news', methods=["POST"])
def save_news():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect('/')
    
    json = request.get_json()
    news_form = NewsForm.from_json(json, meta={'csrf': False})
    
    if news_form.validate():
        url = news_form.data['url']
        title = news_form.data['title']
        description = news_form.data['description']
        date = news_form.data['date']
        image = news_form.data['image']

        print("*************************** DATA I GOT ***************************")
        print(f'URL: {url}--space check')
        print(f'Title: {title}--space check')
        print(f'Description: {description}--space check')
        print(f'Date: {date}--space check')
        print(f'Image: {image}--space check')

        
        news = News.save_news(url=url, title=title, description=description,date=date,image=image)
        new_save = Save(user_id=g.user.id, news_url=news.url)
        db.session.add(new_save)
        db.session.commit()
        # except:
        #     return jsonify(errors="could not save to the database", result=False)
        return jsonify(message="OK", result=True)

    flash('something went wrong with news articles',"danger")
    return jsonify(errors=news_form.errors, result=False)

@app.route('/unsave-news', methods=["POST"])
def unsave_news():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect('/')
    
    url = request.json['url']
    saved = Save.query.get_or_404((g.user.id, url))
    db.session.delete(saved)
    db.session.commit()
    
    return jsonify(message="unsaved successfully", result=True)

@app.route('/saved')
def get_saved_news():
    if not g.user:
        flash("Please login first.", "warning")
        return redirect('/login')
    
