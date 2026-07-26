from app.extensions import db
from datetime import datetime, timezone
from .user import User
from .file import File


class DownloadLog(db.Model):
    __tablename__ = 'download_log'

    id = db.Column(db.Integer, primary_key=True, index=True)
    file_id = db.Column(db.Integer, db.ForeignKey(File.id) ,nullable=False, index=True)
    downloaded_by = db.Column(db.Integer, db.ForeignKey(User.id) ,nullable=False, index=True)
    downloaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    file = db.relationship('File', backref=db.backref('logs', lazy='dynamic'))
    downloader = db.relationship('User', backref=db.backref('downloads', lazy='dynamic'))

    def __repr__(self):
            return f"<File {self.id} for file {self.file_id} by {self.downloaded_by}"


