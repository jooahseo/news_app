""" User View Test """

# run these tests like:
#
#    python -m unittest test_user_view.py

from app import CURR_USER_KEY, app
import os
from unittest import TestCase
from datetime import datetime
from sqlalchemy import exc

from models import db, News, User, Category, Save

os.environ['DATABASE_URL'] = 'postgresql:///news_app_test'


db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for user"""

    def setUp(self):
        """set up user before each testing"""
        db.drop_all()
        db.create_all()

        self.uid = 88
        # create category
        cat = Category.retrieve_or_add('Business')
        self.cat = cat
        # create user
        u = User.signup('testuser', 'test@test.com',
                        'password', cat.id)
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)
        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def save_news(self):
        news = News.save_news('www.test.com', 'testing',
                              'testing is painful but important',
                              datetime.utcnow(), 'www.testimg.url')
        save = Save(user_id=self.u.id, news_url=news.url)
        db.session.add(save)
        db.session.commit()

    def test_main_page_with_without_login(self):
        """check html after sign up"""

        with self.client as c:
            # without login
            res1 = c.get('/')
            self.assertNotIn("Recommended", str(res1.data))

            # with login
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u.id

            res2 = c.get('/')
            self.assertIn("Recommended", str(res2.data))

    def test_invalid_signup(self):
        """check data after signing up with existing username/email"""

        with self.client as c:
            # signup with existing username
            res = c.post('/signup', data=dict(username="testuser",
                                              email="test2@test.com",
                                              password="password",
                                              category="Technology"),
                         follow_redirects=True)
            self.assertIn("Username already taken", str(res.data))

            # signup with existing email
            res2 = c.post('/signup', data=dict(username="testuser2",
                                               email="test@test.com",
                                               password="password",
                                               category="Technology"),
                          follow_redirects=True)
            self.assertIn("Email already exists", str(res2.data))

    def test_invalid_login(self):
        """logging in with invalid credentials"""

        with self.client as c:
            res = c.post('/login', data=dict(username="testuser",
                                             password="wrongpassword"))

            self.assertIn("username or password is not valid", str(res.data))

    def test_profile_page(self):
        """logged in user check profile page"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u.id
            
            res = c.get('/profile')
            self.assertEqual(res.status_code,200)
            self.assertIn("Username", str(res.data))
            self.assertIn("User created at", str(res.data))


    def test_save_page(self):
        """logged in user check 'my save' page"""
        self.save_news()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u.id
            
            res = c.get('/saved')
            self.assertEqual(res.status_code,200)
            self.assertIn("testing is painful but important", str(res.data))

    def test_unauthorized_profile_page(self):
        """unauthorized user's profile page"""

        with self.client as c:
            res = c.get('/profile', follow_redirects=True)

            self.assertEqual(res.status_code,200)
            self.assertIn("Access unauthorized.",str(res.data))

    def test_unauthorized_save_page(self):
        """unauthorized user's profile page"""

        with self.client as c:
            res = c.get('/saved', follow_redirects=True)

            self.assertEqual(res.status_code,200)
            self.assertIn("Please login first.",str(res.data))