from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


# form for user registration
# and user validation
class UserSignUpForm(FlaskForm):
    username = StringField("",validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder":"Username"})
    email = StringField("",validators=[DataRequired(), Email()], render_kw={"placeholder":"Email"})
    password = PasswordField("",validators=[DataRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Password"})
    confirmPassword = PasswordField("", validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder":"Confirm Password"})

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
    username = StringField("", validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder":"Username"})
    companyName = StringField("", validators=[DataRequired(), Length(min=2, max=40)], render_kw={"placeholder":"Company Name"})
    email = StringField("", validators=[DataRequired(), Email()], render_kw={"placeholder":"Email"})
    phoneNumber = StringField("", validators=[DataRequired(), Length(min=10)], render_kw={"placeholder":"Phone"})
    password = PasswordField("", validators=[DataRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Password"})
    confirmPassword = PasswordField("", validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder":"Confirm Password"})
    about = TextAreaField("", validators=[DataRequired(), Length(min=50)], render_kw={"placeholder":"Brief about company not in less than 50 words"})
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
    username = StringField("", validators=[DataRequired()], render_kw={"placeholder":"Username"})
    password = PasswordField("", validators=[DataRequired()], render_kw={"placeholder":"Password"})
    remember_me = BooleanField('Remember')

    submit = SubmitField('Log In')


# form for requesting reset password
class RequestResetForm(FlaskForm):
    email = StringField("", validators=[DataRequired(), Email()], render_kw={"placeholder":"Email"})
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(('There is no account with that email. You must register first.'))


# form for resetting password
class ResetPasswordForm(FlaskForm):
    password = PasswordField("", validators=[DataRequired(), Length(min=4, max=30)], render_kw={"placeholder":"New Password"})
    confirmPassword = PasswordField("", validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder":"Confirm Password"})
    submit = SubmitField('Reset Password')
