from flask import Blueprint, render_template, jsonify, request, flash
from flask_login import login_required
from app.utils.decorators import role_required
from app.services.user_service import UserRole
from app.services.send_email import sendInviteEmail
from app.services.stats import getAdminStats
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
    return render_template('admin/dashboard.html', title='dashboard', stats=stats)


@admin.route('/user-management')
@login_required
@role_required(UserRole.SUPER_ADMIN)
def userManagement():
    users = [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "role": "student",
            "status": "active",
            "year": "2",
            "joined": "Jul 2026"
        },
        {
                    "id": 1,
                    "name": "John Doe",
                    "email": "john@example.com",
                    "role": "student",
                    "status": "active",
                    "year": "2",
                    "joined": "Jul 2026"
                },{
                            "id": 1,
                            "name": "John Doe",
                            "email": "john@example.com",
                            "role": "student",
                            "status": "active",
                            "year": "2",
                            "joined": "Jul 2026"
                        },{
                                    "id": 1,
                                    "name": "John Doe",
                                    "email": "john@example.com",
                                    "role": "student",
                                    "status": "active",
                                    "year": "2",
                                    "joined": "Jul 2026"
                                },{
                                            "id": 1,
                                            "name": "John Doe",
                                            "email": "john@example.com",
                                            "role": "student",
                                            "status": "active",
                                            "year": "2",
                                            "joined": "Jul 2026"
                                        },
                        
    ]
    return render_template('admin/user_management.html', users=users, title='user-management')

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

@admin.route("/invite-user", methods=["POST", 'GET'])
@login_required
@role_required(UserRole.SUPER_ADMIN)
def invite_user():
    form = InviteForm()

    if form.validate_on_submit():
        existing_email = User.query.filter_by(email=form.email.data).first()

        if existing_email():
            flash('User with that email already exists', 'warning')
        #     return re

        # user = User(
        #     username=student["fullname"],
        #     email=email,
        #     year=student["year"]
        # )