"""Create an admin user in the database."""

from project.extensions import db
from project.app import create_app

# Import models
from project.blueprints.users.models import User
import datetime

app = create_app()

# Flask-Admin create admin user
# Create 'username@gmail.com' user with 'admin' role
with app.app_context():
    db.drop_all()
    db.create_all()

    admin_user = User(
        email="user@email.com",
        password="password",
        role="admin"
    )

    db.session.add(admin_user)
    db.session.commit()
