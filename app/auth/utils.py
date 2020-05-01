import os
import secrets
from PIL import Image
from flask import url_for
from app.email import send_email
from flask import current_app

# method for resizing and saving a picture
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (360, 360)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

# password reset method
def send_reset_email(user):
    token = user.get_reset_password_token()

    body = f'''To reset your password, visit the following link:
    {url_for('auth.reset_password', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no change will be made.'''

    send_email('Password Reset Request', sender='noreply@cmalindi.co.za', recipients=[user.email], body=body)