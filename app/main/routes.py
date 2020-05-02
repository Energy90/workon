from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import UserUpdateForm, MessageForm, CompanyUpdateForm
from app.models import User, Message, Notification
from app.main import bp
# from app.auth.utils import save_picture

# home page if not signed in
@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.companies'))
    page = request.args.get('page', 1, type=int)
    company_names = User.query.filter(User.company != None)
    pagination = company_names.order_by(User.company).paginate(
        page, current_app.config['COMPANY_PER_PAGE'], False)
    company = pagination.items
    flash('You are not logged in, loggin so you can view companies profile', 'warning')
    return render_template('main/index.html', title='Home', pagination=pagination, company=company)

# home page once you signed in
@bp.route('/companies', methods=['GET', 'POST'])
@login_required
def companies():
    page = request.args.get('page', 1, type=int)
    company_names = User.query.filter(User.company != None)
    pagination = company_names.order_by(User.company).paginate(
        page, current_app.config['COMPANY_PER_PAGE'], False)
    company = pagination.items 
    return render_template('main/companies.html', title='Companies', pagination=pagination, company=company)


# company full details
@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter(User.company != None).filter_by(username=username).first_or_404()
    return render_template('main/user.html', user=user)

@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter(User.company != None).filter_by(username=username).first_or_404()
    return render_template('main/user_popup.html', user=user)

# rate a company
@bp.route('/rate/<username>')
@login_required
def rate(username):
    user = User.query.filter(User.company != None).filter_by(username=username).first()
    if user is None:
        flash("Company %s not found." % username, 'warning')
        return redirect(url_for('main.user', username=username))
    if user == current_user:
        flash('You cannot rate yourself!', 'warning')
        return redirect(url_for('main.user', username=username))
    current_user.rate(user)
    db.session.commit()
    flash("You rated %s" % username, "primary")
    return redirect(url_for('main.user', username=username))

# unrate a company 
@bp.route('/unrate/<username>')
@login_required
def unrate(username):
    user = User.query.filter(User.company != None).filter_by(username=username).first()
    if user is None:
        flash("Company %s not found." % username, 'warning')
        return redirect(url_for('main.user', username=username))
    if user == current_user:
        flash('You cannot unrate yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.unrate(user)
    db.session.commit()
    flash("You unrated %s" % username, "primary")
    return redirect(url_for('main.user', username=username))

# send message to user or company
@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(sender=current_user, recipient=user, body=form.message.data)
        user.add_notification('unread_message_count', user.new_message())
        db.session.commit()
        flash('Your message has been sent.', "success")
        return redirect(url_for('main.message', username=recipient))
    return render_template('main/send_messages.html', title='Send Message', form=form, recipient=recipient)

# message received
@bp.route('/message')
@login_required
def message():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    pagination = current_user.message_recieved.order_by(
        Message.timestamp.desc()).paginate(
            page, current_app.config['COMPANY_PER_PAGE'], False)
    messages = pagination.items
    return render_template('main/messages.html', messages=messages, pagination=pagination)

# notification
@bp.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])

 # update user information   
@bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    form = UserUpdateForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your changes have been saved', 'success')
        return redirect(url_for('main.update'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('main/update.html', title='Update Profile', form=form)

# update company information
@bp.route('/update_company', methods=['GET', 'POST'])
@login_required
def update_company():
    form = CompanyUpdateForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.company = form.companyName.data
        current_user.email = form.email.data
        current_user.phone = form.phoneNumber.data
        current_user.about = form.about.data
        '''
        if form.logo.data:
            picture_file = save_picture(form.logo.data)
            current_user.image = picture_file
        '''
        db.session.commit()
        flash('Your changes have been saved', 'success')
        return redirect(url_for('main.update_company'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.companyName.data = current_user.company
        form.phoneNumber.data = current_user.phone
        form.about.data = current_user.about
    # image_file = url_for('static', filename='profile_pics/' + current_user.image)
    return render_template('main/update_company.html', title='Company Profile', form=form)