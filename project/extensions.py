"""Define objects of all extensions."""
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
csrf_protect = CSRFProtect()
login_manager = LoginManager()
mail = Mail()