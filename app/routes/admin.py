from flask import Blueprint, render_template
from flask_login import login_required
from app.utils.decorators import role_required

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@admin_blueprint.route('/dashboard')
@login_required
@role_required('admin', 'super_admin')
def dashboard():
    pass

@admin_blueprint.route('/test')
def index():
    return 'Hello World'