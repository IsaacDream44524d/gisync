from flask import Flask
from app.config import Config
from app.utils.vite import vite_assets

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)

    app.config.from_pyfile('config.py', silent=True)

    app.jinja_env.globals["vite_assets"] = vite_assets

    from app.routes.test import main
    app.register_blueprint(main)

    return app