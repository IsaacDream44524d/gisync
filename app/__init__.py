from flask import Flask, url_for, redirect
from app.config import Config
from app.utils.vite import ViteAssets
from app.extensions import migrate, db, login_manager, bcrypt
from dotenv import load_dotenv
from app.utils.handers import errors


load_dotenv()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)

    app.config.from_pyfile('config.py', silent=True)

    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 5, #-> keeps 5 db connections open and reADYD
        'pool_recycle': 1800, #-> closes and refresh any connection that lives forr 1800s to prevent timeout
        'max_overflow': 10 #-> allow 10 extra connection plus pool size when traffic spikes
    }

    # for development only
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SESSION_COOKIES_SAMESITE'] = 'Lax'
    #FOR DEVELOPMENT ONLY

    app.config['SESSION_COOKIES_HTTPONLY'] = True
    app.config['REMEMBER_COOKIES_DURATION'] = 3600 * 24 * 7


    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    migrate.init_app(app, db)

    with app.app_context():
        app.jinja_env.globals["vite"] = ViteAssets()


    from app.routes.admin import admin
    from app.routes.auth import auth
    
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(errors)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app