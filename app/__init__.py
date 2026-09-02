from flask import Flask, app, url_for, redirect, session, request, abort
from app.config import Config
from app.utils.vite import ViteAssets
from app.extensions import migrate, db, login_manager, bcrypt, cache
from app.utils.handers import errors
from flask_login import current_user
from app.models.user import User
import click
from app.services.user_service import UserRole
import os
from dotenv import load_dotenv

# if os.environ.get("FLASK_ENV") == "development":
load_dotenv('.env')  # Load .env file in development mode


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)

    app.config.from_pyfile('config.py', silent=True)

    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 5, #-> keeps 5 db connections open and reADYD
        'pool_recycle': 1800, #-> closes and refresh any connection that lives forr 1800s to prevent timeout
        'max_overflow': 10 #-> allow 10 extra connection plus pool size when traffic spikes
    }

    @app.cli.command("create-admin")
    @click.option("--username", prompt=True)
    @click.option("--email", prompt=True)
    @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
    def create_admin(username, email, password):

        existing = User.query.filter_by(email=email).first()

        if existing:
            click.echo("User already exists.")
            return

        admin = User(
            username=username,
            email=email,
            role=UserRole.ADMIN,
            is_active=True
        )

        admin.setPassword(password)  # Use your existing password method

        db.session.add(admin)
        db.session.commit()

        click.echo(f"Admin {email} created successfully.")

    # for development only
    app.config['SQLALCHEMY_ECHO'] = app.debug
    app.config['SESSION_COOKIES_SAMESITE'] = 'Lax'
    #FOR DEVELOPMENT ONLY

    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['REMEMBER_COOKIE_SECURE'] = True

    from datetime import timedelta

    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)

    app.config['CACHE_TYPE'] = 'SimpleCache'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300
    app.config.from_pyfile('config.py', silent=True)
    

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)

    migrate.init_app(app, db)

    @app.context_processor
    def inject_current_view():
        if current_user.is_authenticated:
            # all user with student role get default student view
            if current_user.role == UserRole.STUDENT:
                current_view = 'student'

            # admin can get current view from session if does not exist set admin as view
            else:
                current_view = session.get('current_view', 'admin')

        # if no view value exists set current view to none
        else:
            current_view = None

        return {'current_view': current_view}

    with app.app_context():
        app.jinja_env.globals["vite"] = ViteAssets()


    # logic for shutting system off for maintenance
    app.config['MAINTENANCE_MODE'] = {
        'admin': True,
        'student': True,
        'main': True,
        'auth': True
    }


    from app.routes.admin import admin
    from app.routes.auth import auth
    from app.routes.main import main
    from app.routes.student import student
    from app.routes.registration import students
    from app.routes.classrep import supervisor
    
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(supervisor, url_prefix='/classrep')
    app.register_blueprint(students, url_prefix='/student')
    app.register_blueprint(errors)
    app.register_blueprint(main)
    app.register_blueprint(student)

    @app.before_request
    def maintenance():
        active_blueprints = request.blueprint

        maintenance_config = app.config.get('MAINTENANCE_MODE', {})

        is_down = maintenance_config.get(active_blueprints, False)

        if is_down:
            abort(503) #service unvailable

    @app.route('/')
    def index():
        # return redirect(url_for('auth.login'))
        return redirect(url_for('students.registrar'))

    return app