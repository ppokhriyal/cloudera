from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from cloudera.models import User

#Login Form
class LoginForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),Email()],render_kw={'autofocus': True})
	password = PasswordField('Password',validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


#RegisterForm
class RegisterForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password',message='Confirm Password must be matching Password')])
	submit = SubmitField('Create Account')
	#Validate Username
	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('This username is already taken. Please choose a diffrent one.')
	#Validate Email
	def Validate_email(self,email):
		user = 	User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('This email is already taken. Please choose a diffrent one.')

#Forgot Password Form
class ForgotPasswordForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),Email()])
	submit = SubmitField('Reset Password')

	#Validate Email
	def validate_email(self,email):
		user = 	User.query.filter_by(email=email.data).first()
		if not user:
			raise ValidationError('This email is not registered. Please choose the valid email id')

#Reset Password Form
class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password',validators=[DataRequired()])
    confirm_new_password = PasswordField('Confirm New Password',validators=[DataRequired(),EqualTo('password',message='Confirm Password must be matching Password')])
    submit = SubmitField('Password Reset')