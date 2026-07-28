from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'Create Password',
        validators=[DataRequired()]
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ]
    )

    submit_btn = SubmitField('Set Password')