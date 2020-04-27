from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from flask_login import current_user

# form for user update
# and user validation

class UserUpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(('That username is taken. Please choose a different username!'))

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(('That email is taken. Please choose a different email!')) 


# form for company update
# and user validation

class CompanyUpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    companyName = StringField('Company Name', validators=[DataRequired(), Length(min=2, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phoneNumber = StringField('Phone (e.g 078)', validators=[DataRequired(), Length(min=10)])
    about = TextAreaField('Brief about the company', validators=[DataRequired(), Length(min=40)])
    logo = FileField('Company Logo', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(('That username is taken. Please choose a different username!'))

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(('That email is taken. Please choose a different email!')) 


# form for sending message

class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=1, max=150)])
    submit = SubmitField('Send')