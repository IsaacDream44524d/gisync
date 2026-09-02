from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, abort, session
from flask_login import login_user, current_user, logout_user, login_required
from app.forms.auth.login import LoginForm
from sqlalchemy import select
from app.models.user import User
from app.extensions import db
from app.services.stats import get_group_stats
from app.services.create_groups import assign_students_to_groups
from app.services.stats import getStudents
from app.utils.validators import FormValidators
from app.models.students import Group
from app.services.groups import cleanup_empty_groups
from app.services.spreadsheet_exporter import generate_groups_excel_buffer
from app.services.supabase_storage import upload_excel_to_supabase


supervisor = Blueprint('supervisor', __name__, url_prefix='/classrep')

# Store last generated download URL in app context or session if needed
latest_export_url = None

@supervisor.route('/dashboard')
@login_required
def dashboard():
    group_stats = get_group_stats(db.session)
    students_page = getStudents(db.session, paginate=True)

    recent_students = students_page.items[:5]

    return render_template('supervisor/supervisor_dashboard.html', title='dashboard', students=recent_students, group_stats=group_stats)


@supervisor.route('/student-management')
@login_required
def students():
    students = getStudents(db.session, paginate=True)
    return render_template('supervisor/student_manager.html', students=students.items, pagination=students, title='students-management')


@supervisor.route('/groups', methods=["GET", "POST"])
@login_required
def groups():
    if request.method == "POST":
        data = request.get_json() or {}
        raw_data = data.get("group_names", "")
        
        try:
            # 1. Parse & Assign students to groups
            groups_list = FormValidators.parse_group_names(raw_data)
            assigned_groups = assign_students_to_groups(db.session, groups_list)

            # 2. Automatically generate Excel & upload to Supabase (30-day signed URL)
            excel_buffer = generate_groups_excel_buffer(db.session)

            if assigned_groups and excel_buffer:
                download_url = upload_excel_to_supabase(excel_buffer, expires_in_seconds=2592000)
            
                # Save the 30-day link in user's browser session
                session['latest_export_url'] = download_url

                return jsonify({
                    "success": True,
                    "message": "Created groups and uploaded 30-day export link to storage",
                    "download_url": download_url
                }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "message": f"Error: {str(e)}"}), 400

    # GET Request
    cleanup_empty_groups(session)
    all_groups = Group.query.all()
    all_students = getStudents(session, paginate=False)
    unassigned_count = len([student for student in all_students if not student.hasGroup()])

    return render_template(
        "supervisor/groups.html",
        title="Groups",
        groups=all_groups,
        unassigned_count=unassigned_count,
        export_url=session.get('latest_export_url')
    )

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
