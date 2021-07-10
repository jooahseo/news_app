""" News view tests """

# run these tests like:
#
#    python -m unittest test_news_view.py

from app import app, CURR_USER_KEY
from flask import jsonify
import os
from unittest import TestCase
from sqlalchemy import exc
from datetime import datetime

from models import db, News, User, Category, Save
from forms import NewsForm

os.environ['DATABASE_URL'] = 'postgresql:///news_app_test'

db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class NewsViewTestCase(TestCase):
    """Test views for news"""

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
                            datetime.utcnow(), 'www.testimg.url' )
        save = Save(user_id=self.u.id, news_url = news.url)
        db.session.add(save)
        db.session.commit()

    # def test_response_after_save_news(self):
    #     """Get response message "OK" after user requests to save the news. """
    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.u.id

    #         res = c.post('/save-news', data=jsonify(url="www.testing.com",
    #                                           title = "testing is fun",
    #                                           description="You should understand how important the testing is",
    #                                           date = datetime.utcnow(),
    #                                           image= "testimgurl"))
    #         print(res.data)
            # self.assertEqual("OK", str(res.data.message))

    def test_user_saved_news(self):
        """After save the news, check html file on user's "my save" page"""
        
        self.save_news()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u.id
            
            res = c.get('/saved')
            
            self.assertEqual(res.status_code,200)
            self.assertIn("My saved news", str(res.data))
            self.assertIn("testing is painful but important", str(res.data))
    
    def test_search_news(self):
        """check html file after user searchs the news"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u.id

            res = c.get('/news?q=bitcoin')
            res2 = c.get('news?q=dlkfjsldfjlsdkfj')

            self.assertEqual(res.status_code, 200)
            self.assertIn('bitcoin', str(res.data))

            self.assertEqual(res2.status_code, 200)
            self.assertIn('No result found for ', str(res2.data))