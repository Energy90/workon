import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # the secrete key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'e4041756bd26481e8e3762e18c5d9b98'

    # sijax configuration
    SIJAX_STATIC_PATH = os.environ.get('AJAX_URL') or \
         os.path.join('.', os.path.dirname(__file__), 'static/js/sijax')
    SIJAX_JSON_URI = os.environ.get('SIJAX_JASON_URI') or '/static/js/sijax/json2.js'

    # database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'workon.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # number of item per page
    COMPANY_PER_PAGE = 12

    # email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('USERNAME')
    MAIL_PASSWORD = os.environ.get('PASSWORD')
    MAIL_USE_SSL = True
    SECURITY_EMAIL_SENDER = os.environ.get('USERNAME')
    MAIL_DEBUG = True
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    ADMINS = ['email']
