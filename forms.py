from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField
from wtforms.validators import InputRequired, Email, url, Length, DataRequired


class UserForm(FlaskForm):
    """Form for user signup"""

    username = StringField("Username",
                           validators=[InputRequired(message="Username required"),
                                       Length(min=4,max=30, message="Username must be between 4 and 30 characters")])
    email = StringField("Email",
                        validators=[InputRequired(message="Email required"),
                                    Email(message="Not a valid Email address")])
    password = PasswordField("Password",
                             validators=[InputRequired("Password required"),
                                         Length(min=6, max=30, message="Password must be between 6 and 30 characters")])
    category = SelectField("I am interested in",
                           choices=[("business", "Business"), ("entertainment", "Entertainment"),
                                    ("health", "Health"), ("science", "Science"),
                                    ("sports", "Sports"), ("technology", "Technology"),("general","General")],
                           validators=[DataRequired(message="Please select the category you're interested in")])

class LoginForm(FlaskForm):
    """User login form"""

    username = StringField("Username",
                           validators=[InputRequired(message="Username required")])

    password = PasswordField("Password",
                             validators=[InputRequired("Password required")])
