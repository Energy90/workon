from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from flask_login import current_user

# form for user update
# and user validation

class UserUpdateForm(FlaskForm):
    username = StringField("", validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder":"Username"})
    email = StringField("", validators=[DataRequired(), Email()], render_kw={"placeholder":"Email"})

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
    username = StringField("", validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder":"Username"})
    companyName = StringField("", validators=[DataRequired(), Length(min=2, max=40)], render_kw={"placeholder":"Company Name"})
    email = StringField("", validators=[DataRequired(), Email()], render_kw={"placeholder":"Email"})
    phoneNumber = StringField("", validators=[DataRequired(), Length(min=10)], render_kw={"placeholder":"Phone"})
    about = TextAreaField("", validators=[DataRequired(), Length(min=100)], render_kw={"placeholder":"Brief about company not in less than 100 characters."})
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
    message = TextAreaField("", validators=[DataRequired(), Length(min=2, max=150)], render_kw={"placeholder":"Message"})
    submit = SubmitField('Send')
