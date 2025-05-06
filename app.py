from flask import Flask
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from models import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change_this_to_something_secure'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simple.db'
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from routes import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# WTForms
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=120)])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

# Create tables before first request (Flask 2.0+ compatible method)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)