from app.extensions import db
from .user import User




class Schedule(db.Model):
    __tablename__ = 'schedule'

    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(200), nullable=False) #OOP makeup class
    type = db.Column(db.String(50), nullable=False) #e.g makeup, holiday cancelled-class, upcoming-test
    subject = db.Column(db.String(100))

    start_time = db.Column(db.DateTime, index=True)
    end_time = db.Column(db.DateTime, index=True)
    version = db.Column(db.Integer, default=1)

    created_by_id = db.Column(db.Integer, db.ForeignKey(User.id) ,nullable=False, index=True)


    creator = db.relationship('User', backref=db.backref('schedules', lazy='dynamic'))

  
    def __repr__(self):
        return f"<Report {self.id} for file {self.file_id} - {self.status})"