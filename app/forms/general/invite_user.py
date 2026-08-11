from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired,Email, Length



class InviteForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    fullname = StringField('Fullname', validators=[DataRequired(), Length(min=5, max=100)])
    role = SelectField('Role', choices=[('student', 'Student'), ('admin', 'Admin'), ('lecture', 'Lecture'), ('super_admin', 'Super admin')])
    submit_btn = SubmitField('Send Invite')

