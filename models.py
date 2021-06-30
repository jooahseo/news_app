from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """connect database via sqlalchemy to Flask app"""
    db.app = app
    db.init_app(app)


class Favorite(db.Model):
    """User's favorites news"""
    __tablename__ = "user_favs"

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete="cascade"),
                        primary_key=True)

    news_id = db.Column(db.Integer,
                        db.ForeignKey('news.id', ondelete="cascade"),
                        primary_key=True)

    user = db.relationship('User')
    news = db.relationship('News')

    def __repr__(self):
        return f"<user_favs User #{self.user_id} {self.user.username} - News #{self.news_id}>"


class News(db.Model):
    """News in the system"""

    __tablename__ = "news"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    author = db.Column(db.String, nullable=False)
    date = db.Column(db.Datetime, nullable=False)
    image = db.Column(db.String)
    url = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    source = db.Column(db.String)

    liked_users = db.relationship(
        'User', secondary="user_favs", backref="fav_news")

    def __repr__(self):
        return f"<News {self.title[0:40]}... from {self.source}>"


class User(db.Model):
    """User in the system"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    category = db.Column(db.String)

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}"

    @classmethod
    def signup(cls, username, email, password, category):
        """sign up user. Hashed password"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            category=category
        )
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """"authenticate a user: check if username and password are valid"""
        
        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
