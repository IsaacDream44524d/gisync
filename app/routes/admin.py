from flask import Blueprint, render_template
from flask_login import current_user, login_required
from app.utils.decorators import role_required
from app.services.user_service import UserRole

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard')
@login_required
@role_required(UserRole.SUPER_ADMIN)
def dashboard():
    print("*****************INSIDE PROTECTED ROUTE")
    print(f"*************current user: {current_user}")
    print(f"***************Authenticated: {current_user.is_authenticated}")
    return render_template('admin/dashboard.html')



@admin.route('/session-test')
def test():
    from flask_login import current_user

    return {
        "Authenticated": current_user.is_authenticated,
        "user-id": current_user.id if current_user.is_authenticated else None
    }