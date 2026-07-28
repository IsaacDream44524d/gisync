from ast import stmt

from flask import Blueprint
from flask import Flask, session, request, url_for, render_template, redirect, flash, abort
from markupsafe import escape
from app.forms.auth.login import LoginForm
from app.forms.auth.resetPassword import RequestResetForm
from app.forms.auth.setPassword import ResetPasswordForm
from app.models import User
from flask_login import login_user, current_user, logout_user
from sqlalchemy import select
from app.extensions import db
from app.services.send_email import sendResetEmail


auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():

        stmt = select(User).where(User.email == form.email.data)

        user = db.session.execute(stmt).scalar_one_or_none()
        if user and user.checkPassword(form.password.data):

            login_user(user,remember=form.remember_me.data)

            if user.isAdmin():
                return redirect(url_for('admin.test'))

            elif user.isSuperAdmin():
                return redirect(url_for('admin.test'))

            return redirect(url_for('admin.test'))

        flash('Invalid credentials', 'warning')

    return render_template('auth/login.html', title='Login', form=form)
     
@auth.route('/Reset-Password', methods=['POST', 'GET'])
def resetRequest():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestResetForm()
    if form.validate_on_submit():

        stmt = select(User).where(User.email == form.email.data)
        user = db.session.execute(stmt).scalar_one_or_none()

        sendResetEmail(user)
        flash(f'A password reset email has been sent to {form.email.data}', 'success')
        return redirect(url_for('auth.login'))
         
    return render_template('auth/reset_request.html', title='Reset password', form=form)

@auth.route('/Reset_Password/<token>', methods=['POST', 'GET'])
def resetForm(token):
    pass




    



