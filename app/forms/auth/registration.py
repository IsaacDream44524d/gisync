from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired,Email
from app.utils.validators import FormValidators



class RegistrationForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email(), FormValidators.classEmail()])
    fullname = StringField('Full Name', validators=[DataRequired()])
    gender = SelectField('Gender', validators=[DataRequired()], default="", choices=[('male', 'Male'), ('female', 'Female'), ("", "Select Gender")])
    submit_btn = SubmitField('Login')

