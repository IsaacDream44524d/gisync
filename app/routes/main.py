from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required
from app.utils.decorators import role_required
from app.services.user_service import UserRole
from app.models.user import User
from app.forms.general.invite_user import InviteForm

main = Blueprint('main', __name__)

# all users routes relocate
@main.route('/profile')
@login_required
def profile():
    return render_template('main/profile.html', title='profile')

@main.route('/settings')
@login_required
def settings():
    form = InviteForm()
    return render_template('main/settings.html', title='settings', form=form)


@main.route('/faq')
@login_required
def faq():
    return render_template('main/faq.html', title='faq')


@main.route('/notifications')
@login_required
def notifications():
    return render_template('main/notifications.html', title='notifications')


@main.route('/calendar')
@login_required
def calendar():
    return render_template('main/calendar.html', title='calendar')