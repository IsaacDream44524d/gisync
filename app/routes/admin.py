from flask import Blueprint, render_template
from flask_login import current_user, login_required
from app.utils.decorators import role_required
from app.services.user_service import UserRole
from app.services.stats import getAdminStats
from app.extensions import db

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard')
@login_required
@role_required(UserRole.SUPER_ADMIN)
def dashboard():
    stats = getAdminStats(db.session)
    print(f'**********************{stats}')
    return render_template('admin/dashboard.html', title='dashboard', stats=stats)


@admin.route('/user-management')
@login_required
@role_required(UserRole.SUPER_ADMIN)
def userManagement():
    return render_template('admin/user_management.html')

@admin.route('/file-management')
@login_required
@role_required(UserRole.SUPER_ADMIN)
def fileManagement():
    return render_template('admin/file_manager.html')

@admin.route('/workflow')
@login_required
@role_required(UserRole.SUPER_ADMIN)
def workflow():
    return render_template('admin/kanban.html')

# all users routes relocate
@admin.route('/profile')
@login_required
@role_required(UserRole.SUPER_ADMIN)
def profile():
    return render_template('profile.html')



@admin.route('/settings')
@login_required
@role_required(UserRole.SUPER_ADMIN)
def settings():
    return render_template('settings.html')



@admin.route('/faq')
@login_required
@role_required(UserRole.SUPER_ADMIN)
def faq():
    return render_template('faq.html')






@admin.route('/notifications')
@login_required
@role_required(UserRole.SUPER_ADMIN)
def notifications():
    return render_template('notifications.html')


@admin.route('/calendar')
@login_required
@role_required(UserRole.SUPER_ADMIN)
def calendar():
    return render_template('calendar.html')

#AFTER CREATING A USER OR UPLOADING A FILE DO 'cache.delete(admin-stats)'



