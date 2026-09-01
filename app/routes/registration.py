from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.forms.auth.registration import RegistrationForm
from app.models.students import Student
from app.extensions import db
from app.models.enums import Gender



students = Blueprint('students', __name__, url_prefix='/student')

@students.route('/registration', methods=['GET', 'POST'])
def registrar():

    form = RegistrationForm()
    success = session.pop('form_success', False)

    if form.validate_on_submit():

        # save student
        existing_email = Student.query.filter_by(email=form.email.data).first()
        
        if existing_email:
            flash('Student already registered', 'warning')
            return redirect(url_for('students.registrar'))
        
        student = Student(
            username=form.fullname.data,
            email=form.email.data,
            gender = Gender(form.gender.data.lower()),
        )
        

        
        db.session.add(student)
        db.session.commit()

        session['form_success'] = True

        return redirect(url_for('students.registrar'))


    return render_template('auth/registration.html', title='registration', form=form, success=success)