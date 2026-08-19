from flask import redirect, render_template, current_app as app, Blueprint

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/page_404.html', title='page not found'), 404

@errors.app_errorhandler(403)
def access_denied_page(error):
    return render_template('errors/page_403.html', title='forbidden'), 403

@errors.app_errorhandler(500)
def internal_server_error(error):
    return render_template('errors/page_404.html', title='server error'), 500



