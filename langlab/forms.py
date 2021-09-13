from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError



class LoginForm(FlaskForm):
	username = StringField('Username',
							validators=[DataRequired(), Length(min=2, max=20)])
	password = PasswordField('Password',
							validators=[DataRequired(), Length(min=8)])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')
