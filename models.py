from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """connect database via sqlalchemy to Flask app"""
    db.app = app
    db.init_app(app)


class Save(db.Model):
    """User's saved news"""
    __tablename__ = "user_save"

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete="cascade"),
                        primary_key=True)

    news_url = db.Column(db.String,
                         db.ForeignKey('news.url', ondelete="cascade"),
                         primary_key=True)

    user = db.relationship('User')
    news = db.relationship('News')

    def __repr__(self):
        return f"<user_save User #{self.user_id} {self.user.username} - News #{self.news_url}>"


class News(db.Model):
    """News in the system"""

    __tablename__ = "news"

    url = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    image = db.Column(db.Text,
                      default="/static/image/news.png" )

    saved_user = db.relationship('User',
                                  secondary="user_save", 
                                  backref="saved_news")

    def __repr__(self):
        return f"<News {self.title[0:40]}... from {self.url[0:40]}...>"

    @classmethod
    def save_news(cls, url, title, description, date, image):
        news = cls.query.filter_by(url=url).first()

        if news:
            return news
        else:
            news = News(url=url, title=title, description=description, 
                        date=date, image=image)
            db.session.add(news)
            db.session.commit()
            return news

class User(db.Model):
    """User in the system"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete="set null"))

    interest = db.relationship('Category', backref="users")

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}"

    def is_news_saved(self, url):
        """Is this news' url in the user's save?"""

        news = Save.query.get((self.id, url))
        return True if news else False
        # found_news = [news for news in self.saved_news if news.url == url]
        # return len(found_news) == 1

    @classmethod
    def signup(cls, username, email, password, category_id):
        """sign up user. Hashed password"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            category_id=category_id
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


class Category(db.Model):
    """news category"""

    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)

    @classmethod
    def retrieve_or_add(cls, name):
        category = cls.query.filter_by(name=name).first()

        if not category:
            category = Category(name=name)
            db.session.add(category)
            db.session.commit()  

        return category