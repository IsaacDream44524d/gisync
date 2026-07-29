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
        return redirect(url_for('admin.dashboard'))

    form = LoginForm()

    if form.validate_on_submit():

        stmt = select(User).where(User.email == form.email.data)
        user = db.session.execute(stmt).scalar_one_or_none()

        if user is None and not user.checkPassword(form.password.data):
            flash('Invalid credentials', 'warning')
            return redirect('auth.login')

        print("*****************BEFORE login_user")
        print(f"*************current user: {current_user}")
        print(f"***************Authenticated: {current_user.is_authenticated}")

       
        login_user(user, remember=form.remember_me.data)

        print("*****************AFTER login_user")
        print(f"*************current user: {current_user}")
        print(f"***************Authenticated: {current_user.is_authenticated}")

        #redirect user to the page they wanted
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('admin.dashboard')

        return redirect(next_page)

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
        flash(f'If an account for {form.email.data} exist, a reset email has been sent', 'success')
        return redirect(url_for('auth.login'))
         
    return render_template('auth/reset_request.html', title='Reset password', form=form)

@auth.route('/trial', methods=['POST', 'GET'])
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



    



