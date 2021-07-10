""" News Model Test """

# run these tests like:
#
#    python -m unittest test_news_model.py

import os
from unittest import TestCase
from datetime import datetime

from models import db, News, User, Category, Save

os.environ['DATABASE_URL'] = 'postgresql:///news_app_test'

from app import app

db.drop_all()
db.create_all()

class NewsModelTestCase(TestCase):
    """"Test news model"""

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

    def test_news_create(self):
        """Does save_news method from news model work?"""
        news = News.save_news('www.testing.com', 'testing', 'testing is painful but important', datetime.utcnow(), 'www.sometestimg.url' )
        news_created = News.query.get(news.url)

        all_news = News.query.all()

        self.assertEqual(len(all_news), 1)
        self.assertEqual(news, news_created)

    def test_news_save(self):
        """When a user saves the news, 
            Does news save to the user_save table?"""

        news = News.save_news('www.testing.com', 'testing', 'testing is painful but important', datetime.utcnow(), 'www.sometestimg.url' )
        save = Save(user_id=self.u.id, news_url=news.url)
        db.session.add(save)
        db.session.commit()

        get_save = Save.query.get((self.u.id, news.url))
        all_save = Save.query.all()

        self.assertEqual(len(all_save),1)
        self.assertEqual(get_save.user_id, self.u.id)
        self.assertEqual(get_save.news_url, news.url)

    



