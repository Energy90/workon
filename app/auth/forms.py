from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


# form for user registration
# and user validation
class UserSignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(('That username is taken. Please choose a different username!'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(('That email is taken. Please choose a different email!'))


# form company registration
class CompanySignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    companyName = StringField('Company Name', validators=[DataRequired(), Length(min=2, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phoneNumber = StringField('Phone (e.g 078)', validators=[DataRequired(), Length(min=10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    about = TextAreaField('Brief about the company', validators=[DataRequired(), Length(min=40)])
    logo = FileField('Company Logo', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png'])])

    submit = SubmitField('Sign Up')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(('That username is taken. Please choose a different username!'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(('That email is taken. Please choose a different email!')) 


# form for login
class LogInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember')

    submit = SubmitField('Log In')


# form for resetting
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(('There is no account with that email. You must register first.'))


# form for resetting password
class ResetPasswordForm(FlaskForm):
    password = StringField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')