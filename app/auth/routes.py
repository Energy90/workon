from flask import (render_template, redirect, url_for, flash, request)
from werkzeug.urls import url_parse, url_encode
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.auth.forms import (LogInForm, UserSignUpForm, RequestResetForm, ResetPasswordForm, CompanySignUpForm)
from app.models import User
from app.auth.utils import save_picture, send_reset_email

# login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.companies'))
    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.companies')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)

# logout
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# register
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.companies'))
    form = UserSignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Sign Up', form=form)

# register company
@bp.route('/register_company', methods=['GET', 'POST'])
def register_company():
    if current_user.is_authenticated:
        return redirect(url_for('main.companies'))
    form = CompanySignUpForm()
    if form.validate_on_submit():
        picture = save_picture(form.logo.data)
        user = User(username=form.username.data, email=form.email.data, about=form.about.data, image=picture, company=form.companyName.data, phone=form.phoneNumber.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a register user!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register_company.html', title='Sign Up', form=form)

# request reset password
@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.companies'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash('Check your email for the instructions to reset your password', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)

# reset password
@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.companies'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)