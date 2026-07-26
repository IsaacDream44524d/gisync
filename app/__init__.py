from flask import Flask
from app.config import Config
from app.utils.vite import vite_assets
from app.extensions import migrate, db, login_manager, bcrypt
from app import models
from dotenv import load_dotenv


load_dotenv()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)

    app.config.from_pyfile('config.py', silent=True)

    app.jinja_env.globals["vite_assets"] = vite_assets


    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    migrate.init_app(app, db)

    from app.routes.admin import admin_blueprint
    app.register_blueprint(admin_blueprint)

    return app