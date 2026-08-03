from app.extensions import db
from datetime import datetime, timezone
from sqlalchemy import UniqueConstraint
from .file import File
from .user import User




class Notification(db.Model):
    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True, index=True)
    message = db.Column(db.text, nullable=False) #actual notification
    type = db.Column(db.String(50), nullable=False) #notification type e.g new-file, new-schedule, update-schedule

    file_id = db.Column(db.Integer, db.ForeignKey(File.id) ,nullable=True, index=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey(Schedule.id) ,nullable=True, index=True)

    created_by_id = db.Column(db.Integer, db.ForeignKey(User.id) ,nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    is_read = db.Column(db.Boolean, default=False)
    Target_role = db.Column(db.String(50))

    
    
    posted_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    

    file = db.relationship('File', backref=db.backref('reports', lazy='dynamic', cascade='all, delete-orphan'))
    creater = db.relationship('User', backref=db.backref('reports', lazy='dynamic'))

 
    def __repr__(self):
        return f"<notification {self.id} for file {self.file_id} or schedule {self.schedule_id} by - {self.created_by_id})"