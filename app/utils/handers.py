from flask import redirect, render_template, current_app as app, Blueprint

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/page_404.html'), 404

@errors.app_errorhandler(403)
def access_denied_page(error):
    return render_template('errors/page_403.html'), 403

@errors.app_errorhandler(500)
def internal_server_error(error):
    return render_template('errors/page_404.html'), 500



