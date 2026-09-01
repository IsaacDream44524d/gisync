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
from flask_login import current_user, login_required
from app.utils.decorators import role_required


auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role.value == 'student':
            session['current_view'] = 'student'
            return redirect(url_for('student.dashboard'))

        session['current_view'] = 'admin'
        return redirect(url_for('admin.dashboard'))

    form = LoginForm()

    if form.validate_on_submit():

        stmt = select(User).where(User.email == form.email.data)
        user = db.session.execute(stmt).scalar_one_or_none()

        if user is None or not user.checkPassword(form.password.data):
            flash('Invalid credentials', 'warning')
            return redirect(url_for('auth.login'))
       
        login_user(user, remember=form.remember_me.data)

        #redirect user to the page they wanted

        login_user(user, remember=form.remember_me.data)

        # next_page = request.args.get('next')

        # if next_page and next_page.startswith('/'):
        #     return redirect(next_page)

        # if user.role.value == 'student':
        #     return redirect(url_for('student.dashboard'))

        # return redirect(url_for('admin.dashboard'))
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):

            if current_user.is_authenticated:

                if current_user.role.value == 'student':
                    next_page = url_for('student.dashboard')
                
                else:
                    next_page = url_for('admin.dashboard')
                    
            next_page = url_for('auth.login')


        return redirect(next_page)

    return render_template('auth/login.html', title='Login', form=form)
                

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('auth.login'))

    
     
@auth.route('/Reset-Password', methods=['POST', 'GET'])
def resetRequest():
    if current_user.is_authenticated:
        if current_user.role.value == 'student':
            return redirect(url_for('student.dashboard'))
        return redirect(url_for('admin.dashboard'))

    form = RequestResetForm()
    if form.validate_on_submit():

        stmt = select(User).where(User.email == form.email.data)
        user = db.session.execute(stmt).scalar_one_or_none()

        sendResetEmail(user)
        flash(f'If an account for {form.email.data} exist, a reset email has been sent', 'success')
        return redirect(url_for('auth.login'))
         
    return render_template('auth/reset_request.html', title='Reset password', form=form)

@auth.route('/', methods=['POST', 'GET'])
def reset():
    if current_user.is_authenticated:
        return redirect(url_for('admin.test'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():

        flash(f'Password updated successfully, proceed with login', 'success')
        return redirect(url_for('auth.login'))
            
    return render_template('auth/reset.html', title='Create password', form=form)
    
    

@auth.route('/Reset-Password/<token>', methods=['POST', 'GET'])
def resetForm(token):
    pass



    



