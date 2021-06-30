import os
from flask import Flask, flash, render_template, redirect, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
import requests

from models import db, connect_db, News, User
from keys import API_KEY

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///news')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a top secret")

