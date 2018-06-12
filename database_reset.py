"""Create an admin user in the database."""

from project.extensions import db
from project.app import create_app

app = create_app()

# Keep database tables but delete all information
with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.commit()
