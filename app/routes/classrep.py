from flask import Blueprint, render_template, request, flash, redirect, url_for, session, abort
from flask_login import login_user, current_user, logout_user, login_required
from app.forms.auth.login import LoginForm
from app.forms.auth.resetPassword import RequestResetForm
from app.forms.auth.setPassword import ResetPasswordForm
from sqlalchemy import select
from app.models.user import User
from app.extensions import db
from app.utils.decorators import role_required
from app.services.stats import getStudents


supervisor = Blueprint('supervisor', __name__, url_prefix='/classrep')


@supervisor.route('/dashboard')
@login_required
def dashboard():
    return render_template('supervisor/supervisor_dashboard.html', title='dashboard')


@supervisor.route('/student-management')
@login_required
def students():
    students = getStudents(db.session)
    return render_template('supervisor/student_manager.html', students=students.items, pagination=students, title='students-management')

@supervisor.route('/groups')
@login_required
def groups():
    group_names = request.form.get("group_names", "")
    print(f'***************{group_names}')
    return render_template('supervisor/groups.html', title='Groups')

@supervisor.route('/login', methods=['GET', 'POST'])
def login():

    # Already logged in
    if current_user.is_authenticated:
        return redirect(url_for('supervisor.dashboard'))

    form = LoginForm()

    if form.validate_on_submit():

        stmt = select(User).where(User.email == form.email.data)
        user = db.session.execute(stmt).scalar_one_or_none()

        # Invalid credentials
        if user is None or not user.checkPassword(form.password.data):
            flash('Invalid credentials', 'warning')
            return redirect(url_for('supervisor.login'))

        # Block students and users without a role
        if user.role is None or user.role.value == 'student':
            abort(403)

        # Log user in
        login_user(user, remember=form.remember_me.data)

        # Redirect to originally requested page if safe
        next_page = request.args.get('next')

        if not next_page or not next_page.startswith('/'):
            next_page = url_for('supervisor.dashboard')

        return redirect(next_page)

    return render_template('auth/login.html',title='Login',form=form)



@supervisor.route('/logout')
# @role_required(UserRole.SUPER_ADMIN)
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('supervisor.login'))
