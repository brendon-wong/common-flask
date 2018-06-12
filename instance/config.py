"""Production Flask config settings."""

# The instance folder is not supposed to be committed to version control

# Flask Settings

ENV = 'production'
DEBUG = False

SECRET_KEY = 'this_is_an_insecure_non_production_key'

# Flask-SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'postgres://'
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids SQLAlchemy warning

# Flask-Mail SMTP server settings for Gmail
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = 'username@gmail.com'
MAIL_PASSWORD = 'password'
MAIL_DEFAULT_SENDER = '"Project" <username@gmail.com>'
