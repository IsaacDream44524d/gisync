from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required
from app.utils.decorators import role_required
from app.services.user_service import UserRole
from app.services.send_email import sendInviteEmail
from app.services.stats import getAdminStats, getAllStudents
from app.extensions import db
from app.utils.spreadsheet_reader import extract_students
from app.models.user import User
from app.forms.general.invite_user import InviteForm

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard')
@login_required
@role_required(UserRole.SUPER_ADMIN)
def dashboard():
    stats = getAdminStats(db.session)
    form = InviteForm()
    return render_template('admin/dashboard.html', title='dashboard', stats=stats, form=form)


@admin.route('/user-management')
@login_required
@role_required(UserRole.SUPER_ADMIN)
def userManagement():
    stats = getAdminStats(db.session)
    form = InviteForm()
    users = getAllStudents(db.session, db.select)
    return render_template('admin/user_management.html', form=form, users=users, stats=stats, title='user-management')

@admin.route('/file-management')
@login_required
@role_required(UserRole.SUPER_ADMIN)
def fileManagement():
    return render_template('admin/file_manager.html', title='file-management')

@admin.route('/workflow')
@login_required
@role_required(UserRole.SUPER_ADMIN)
def workflow():
    return render_template('admin/kanban.html', title='workflow')

# all users routes relocate
@admin.route('/profile')
@login_required
@role_required(UserRole.SUPER_ADMIN)
def profile():
    return render_template('profile.html', title='profile')


@admin.route('/settings')
@login_required
@role_required(UserRole.SUPER_ADMIN)
def settings():
    form = InviteForm()
    return render_template('settings.html', title='settings', form=form)


@admin.route('/faq')
@login_required
@role_required(UserRole.SUPER_ADMIN)
def faq():
    return render_template('faq.html', title='faq')


@admin.route('/notifications')
@login_required
@role_required(UserRole.SUPER_ADMIN)
def notifications():
    return render_template('notifications.html', title='notifications')


@admin.route('/calendar')
@login_required
@role_required(UserRole.SUPER_ADMIN)
def calendar():
    return render_template('calendar.html', title='calendar')

#AFTER CREATING A USER OR UPLOADING A FILE DO 'cache.delete(admin-stats)'

@admin.route("/resources/import", methods=["POST"])
@login_required
@role_required(UserRole.SUPER_ADMIN)
def import_resource():
    file = request.files.get("file")
    category = request.form.get("category")

    if not file:
        return jsonify({"error": "No file provided"}), 400
    
    extension = file.filename.rsplit(".", 1)[-1].lower()

    if extension != "xlsx":
        return jsonify({"error": "File Not Supported"}), 400

    if category != "students":
        return jsonify({"error": "Unsupported category"}), 400

    try:
        students, errors = extract_students(file=file)

        emails = {
            student["email"].lower()
            for student in students
        }

        existing_emails = {
            email.lower()
            for (email,) in (
                db.session.query(User.email)
                .filter(User.email.in_(emails))
                .all()
            )
        }

        users_to_create = []
        skipped = []

        for student in students:
            email = student["email"].lower()

            if email in existing_emails:
                skipped.append(email)
                continue

            user = User(
                username=student["fullname"],
                email=email,
                year=student["year"]
            )

            user.setUnusablePassword()

            users_to_create.append(user)
            existing_emails.add(email)

        if not users_to_create:
            return jsonify({
                "message": f"No new users found. {len(skipped)} skipped."
            }), 200

        db.session.add_all(users_to_create)
        db.session.commit()

        # Send invites after successful commit
        for user in users_to_create:
            sendInviteEmail(user)

        return jsonify({
            "message": (
                f"Created {len(users_to_create)} account/s "
                f"and skipped {len(skipped)} existing user/s."
            ),
            "error": errors,
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@admin.route("/invite-user", methods=["POST"])
@login_required
@role_required(UserRole.SUPER_ADMIN)
def inviteUser():
    roles = {
        'super_admin': UserRole.SUPER_ADMIN,
        'admin': UserRole.ADMIN,
        'student': UserRole.STUDENT
    }

    form = InviteForm()

    if not form.validate_on_submit():
        return jsonify({
            'error': form.errors
        }), 400

    existing_email = User.query.filter_by(email=form.email.data).first()

    if existing_email:
        return jsonify({
            'error': ['User with that email already exists']
        }), 400

    role = roles.get(form.role.data)

    if not role:
        return jsonify({
            'error': ['Invalid role selected']
        }), 400

    user = User(
        username=form.fullname.data,
        email=form.email.data,
        role=role
    )

    user.setUnusablePassword()

    db.session.add(user)
    db.session.commit()

    sendInviteEmail(user)

    return jsonify({
        'message': f'Invite email sent to {form.email.data} as {form.role.data}'
    }), 200