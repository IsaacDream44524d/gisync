from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired,Email, Length



class notificationForm(FlaskForm):
    message = StringField('Message', validators=[DataRequired()])
    title = StringField('Message', validators=[DataRequired()])
    type = SelectField('Notification Type', choices=[('general_announcement', 'General Announcement'), ('Academic Update', 'academic_update'), ('important_notice', 'important_notice'), ('event_reminder', 'Event Reminder'), ('urgent_alert', 'Urgent Alert')])
    submit_btn = SubmitField('Send Invite')
