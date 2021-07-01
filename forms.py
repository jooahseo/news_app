from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField
from wtforms.validators import InputRequired, Email, url, Length, DataRequired


class UserForm(FlaskForm):
    """Form for user signup"""

    username = StringField("Username",
                           validators=[InputRequired(message="Username required"),
                                       Length(min=4, message="Username must be more than 4 characters")])
    email = StringField("Email",
                        validators=[InputRequired(message="Email required"),
                                    Email(message="Not a valie Email address")])
    password = PasswordField("Password",
                             validators=[InputRequired("Password required"),
                                         Length(min=6, max=30, message="Password must be between 6 and 30 characters")])
    category = SelectField("I am interested in",
                           choices=[("business", "Business"), ("entertainment", "Entertainment"),
                                    ("health", "Health"), ("science", "Science"),
                                    ("sports", "Sports"), ("technology", "Technology")],
                           validators=[InputRequired(message="Please select the category you're interested in")])
