"""Development Flask config settings."""

import os

# Flask Settings

ENV = 'development'
DEBUG = True

# SERVER_NAME = 'localhost:5000'
SECRET_KEY = 'this_is_an_insecure_development_key'

# Flask-SQLAlchemy settings
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Local sqlite3 database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
# Local copy of remote Heroku Postgres db to generate migration script locally:
# SQLALCHEMY_DATABASE_URI = "postgresql://localhost/heroku_remote_database"
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids SQLAlchemy warning

# Flask-Mail SMTP server settings for Yahoo
MAIL_SERVER = 'smtp.mail.yahoo.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = 'username@yahoo.com'
MAIL_PASSWORD = 'password'
MAIL_DEFAULT_SENDER = '"Project" <username@yahoo.com>'
# Have Flask-Mail not send emails for testing
# MAIL_SUPPRESS_SEND = True
