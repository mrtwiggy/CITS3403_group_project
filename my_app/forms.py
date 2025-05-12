from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField, SelectField, HiddenField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo

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

# Form definition
class ReviewForm(FlaskForm):
    franchise_id = SelectField('Franchise', validators=[DataRequired()], 
                              coerce=int)
    
    location_id = SelectField('Location', validate_choice=False,
                                      coerce=int)
    
    drink_name = StringField('Drink Name', validators=[DataRequired()])
    
    drink_size = RadioField('Size', choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')],
                           validators=[DataRequired()])
    
    # Hidden fields to store button selections
    sugar_level = HiddenField('Sugar Level', validators=[DataRequired()])
    ice_level = HiddenField('Ice Level', validators=[DataRequired()])
    
    review_content = TextAreaField('Your Review', validators=[DataRequired(), Length(min=5, max=500)])
    
    rating = HiddenField('Rating', validators=[DataRequired()])
    
    submit = SubmitField('Submit')