from flask import Blueprint, render_template
from flask_login import current_user, login_required
from app.utils.decorators import role_required
from app.services.user_service import UserRole

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard')
@login_required
@role_required(UserRole.SUPER_ADMIN)
def dashboard():
    return render_template('admin/dashboard.html')


@admin.route('/user-management')
@login_required
@role_required(UserRole.SUPER_ADMIN)
def userManagement():
    return render_template('admin/user_management.html')