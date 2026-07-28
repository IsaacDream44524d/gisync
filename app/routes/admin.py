from flask import Blueprint, render_template
from flask_login import login_required
from app.utils.decorators import role_required

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard')
@login_required
@role_required('admin', 'super_admin')
def dashboard():
    pass

@admin.route('/tets')
def test():
    return 'Hello World'