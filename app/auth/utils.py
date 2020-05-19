import os
import secrets
from flask import url_for
from app.email import send_email
from flask import current_app


# password reset method
def send_reset_email(user):
    token = user.get_reset_password_token()

    body = f'''To reset your password, visit the following link:
    {url_for('auth.reset_password', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no change will be made.'''

    send_email('Password Reset Request', sender='noreply@cmalindi.co.za', recipients=[user.email], body=body)