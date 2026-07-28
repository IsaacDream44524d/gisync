from app.extensions import db
from datetime import datetime, timezone
import enum
from sqlalchemy import UniqueConstraint
from .file import File
from .user import User
from .enums import ReportStatus




class Report(db.Model):
    __tablename__ = 'report'

    id = db.Column(db.Integer, primary_key=True, index=True)
    file_id = db.Column(db.Integer, db.ForeignKey(File.id, ondelete='CASCADE') ,nullable=False, index=True)
    reported_by = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE') ,nullable=False, index=True)

    status = db.Column(db.Enum(ReportStatus), default=ReportStatus.PENDING, nullable=False, index=True)
    reason = db.Column(db.String(500), nullable=False)
    
    resolved_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    created_at = db.Column(db.DateTime)

    file = db.relationship('File', backref=db.backref('reports', lazy='dynamic', cascade='all, delete-orphan'))
    reporter = db.relationship('User', backref=db.backref('reports', lazy='dynamic'))

    #prevents same user from reporting same file twice
    __table_args__ = (
        UniqueConstraint('file_id', 'reported_by', name='uq_file_reporter'),
    )

    def __repr__(self):
        return f"<Report {self.id} for file {self.file_id} - {self.status})"