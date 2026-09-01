from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_caching import Cache


db = SQLAlchemy()
login_manager = LoginManager()
# login_manager.login_view= 'auth.login'
login_manager.login_view= 'supervisor.login'
login_manager.login_message_category = 'warning'
migrate = Migrate()
bcrypt = Bcrypt()
cache = Cache()