from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required


student = Blueprint('student', __name__)

@student.route('/dashboard')
@login_required
def dashboard():
    return render_template('student/student_dashboard.html', title='dashboard')

@student.route('/test')
@login_required
def tests():
    pass

@student.route('/timetable')
@login_required
def timetable():
    pass

@student.route('/exams')
@login_required
def exams():
    pass


@student.route('/downloads')
@login_required
def downloads():
    pass

@student.route('/notes')
@login_required
def notes():
    return render_template('student/notes.html', title='notes')