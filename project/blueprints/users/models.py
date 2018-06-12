"""User models."""
import datetime as dt

from project.extensions import db, bcrypt
from flask_login import UserMixin


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    # Authentication

    # 128 characters is a sensible default for the max length of full names
    full_name = db.Column(db.String(128))
    # What should we call you? (for example, when we send you email?)
    preferred_name = db.Column(db.String(128))
    # 254 characters is the maximum length of an email address
    email = db.Column(db.String(254), unique=True, nullable=False)
    email_confirmed = db.Column(db.Boolean, default=False, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    role = db.Column(db.String(128))

    # Activity tracking
    created_at = db.Column(db.DateTime, nullable=False,
                           default=dt.datetime.utcnow)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor
        super(User, self).__init__(**kwargs)
        # Custom setup
        self.password = User.encrypt_password(kwargs['password'])

    @classmethod
    def encrypt_password(cls, password):
        return bcrypt.generate_password_hash(password).decode('UTF-8')

    @classmethod
    def authenticate(cls, email, password):
        found_user = cls.query.filter_by(email=email).first()
        if found_user:
            authenticated_user = bcrypt.check_password_hash(
                found_user.password, password)
            if authenticated_user:
                # Return the user in the event we want to store information in the session
                return found_user
        return False

    def __repr__(self):
        return f"{self.name}"
