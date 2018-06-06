"""User blueprint."""

# from flask import Blueprint, render_template
from flask import Blueprint, render_template_string, url_for

from flask_login import login_required
from project.blueprints.users.decorators import roles_required

# users = Blueprint('users', __name__, template_folder='templates')
users = Blueprint('users', __name__)

