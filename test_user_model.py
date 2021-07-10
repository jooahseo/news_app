""" User Model Test """

# run these tests like:
#
#    python -m unittest test_user_model.py

import os
from unittest import TestCase
from datetime import datetime
from sqlalchemy import exc

from models import db, News, User, Category, Save

os.environ['DATABASE_URL'] = 'postgresql:///news_app_test'

from app import app

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """"Test user model"""

    def setUp(self):
        """set up user before each testing"""
        db.drop_all()
        db.create_all()

        self.uid = 1000
        # create category 
        cat = Category.retrieve_or_add('Business')
        self.cat = cat
        # create user 
        u = User.signup('testuser', 'test@test.com', 'password', cat.id)
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)
   
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def save_news(self):
        news = News.save_news('www.test.com', 'testing', 
                            'testing is painful but important', 
                            datetime.utcnow(), 'www.testimg.url' )
        save = Save(user_id=self.u.id, news_url = news.url)
        db.session.add(save)
        db.session.commit()

    def test_signup_user_category(self):
        """category check after signup"""

        # create new catetogy and user
        new_cat = Category.retrieve_or_add('Science')
        u2 = User.signup('testuser2', 'test2@test.com', 'password', new_cat.id)
        db.session.commit()
        
        self.assertEqual(u2.interest, new_cat)
        self.assertNotEqual(self.u.interest, new_cat)
        self.assertEqual(self.u.interest.name, "Business")

    def test_invalid_username_signup(self):
        """sign up with existing username"""

        #signup with existing username
        u2 = User.signup('testuser','test2@test.com','password',self.cat.id)
        with self.assertRaises(exc.IntegrityError):
            db.session.commit()

    def test_invalid_email_signup(self):
        """sign up with existing email address"""

        u2 = User.signup('testuser2','test@test.com','password',self.cat.id)
        with self.assertRaises(exc.IntegrityError):
            db.session.commit() 

    def test_authenticate(self):
        """Does authenticate method work?"""

        #correct credentials
        res = User.authenticate('testuser','password')
        self.assertEqual(res,self.u)

        #incorrect credentials
        res2 = User.authenticate('testuser','wrongpassword')
        self.assertFalse(res2)

    def test_is_news_saved(self):
        """Does is_news_saved method work?"""

        self.save_news()
        news = News.query.get('www.test.com')
        res = self.u.is_news_saved(news.url)

        self.assertTrue(res)

        u2 = User.signup('testuser2','test2@test.com','password',self.cat.id)
        res2 = u2.is_news_saved(news.url)

        self.assertFalse(res2)