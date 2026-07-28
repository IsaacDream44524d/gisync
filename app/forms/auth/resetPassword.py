from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired, Email




class RequestResetForm(FlaskForm):
    email = StringField(
        'Email Address',
        validators=[DataRequired(), Email()]
    )

    submit_btn = SubmitField('Reset Request')

