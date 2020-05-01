import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'e4041756bd26481e8e3762e18c5d9b98'
'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'workon.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    COMPANY_PER_PAGE = 12
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('USERNAME')
    MAIL_PASSWORD = os.environ.get('PASSWORD')
    MAIL_USE_SSL = True
    SECURITY_EMAIL_SENDER = os.environ.get('USERNAME')
    MAIL_DEBUG = True
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    ADMINS = ['cmalindi@gmail.com']