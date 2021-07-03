from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField
from wtforms.validators import InputRequired, Email, url, Length, DataRequired

news_category = [("Business", "Business"), ("Entertainment", "Entertainment"),
                 ("Health", "Health"), ("Science", "Science"),
                 ("Sports", "Sports"), ("Technology", "Technology"), ("General", "General")]

class UserEditForm(FlaskForm):
    """Form for user profile edit"""

    email = StringField("Email",
                        validators=[InputRequired(message="Email required"),
                                    Email(message="Not a valid Email address")])

    category = SelectField("I am interested in",
                           choices = news_category,
                           validators=[DataRequired(message="Please select the category you're interested in")])


class UserForm(FlaskForm):
    """Form for user signup"""

    username = StringField("Username",
                           validators=[InputRequired(message="Username required"),
                                       Length(min=4, max=30, message="Username must be between 4 and 30 characters")])
    email = StringField("Email",
                        validators=[InputRequired(message="Email required"),
                                    Email(message="Not a valid Email address")])
    password = PasswordField("Password",
                             validators=[InputRequired("Password required"),
                                         Length(min=6, max=128, message="Password must be longer than 6 characters")])
    category = SelectField("I am interested in",
                           choices = news_category,
                           validators=[DataRequired(message="Please select the category you're interested in")])


class LoginForm(FlaskForm):
    """User login form"""

    username = StringField("Username",
                           validators=[InputRequired(message="Username required")])

    password = PasswordField("Password",
                             validators=[InputRequired("Password required")])
