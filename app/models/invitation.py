from app.extensions import db
from datetime import datetime, timezone
from .enums import UserRole

class Invitation(db.Model):
    __tablename__ = 'invitation'

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(25), nullable=False, unique=True, index=True)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    invited_by_id = db.Column(db.Integer, nullable=True, index=True)
    is_used = db.Column(db.Boolean, default=False, index=True)
    role = db.Column(db.Enum(UserRole), default=UserRole.STUDENT, nullable=False, index=True)
    created_at = db.Column(db.DateTime, index=True, default=lambda: datetime.now(timezone.utc))


    def __repr__(self):
            return f"<Invited {self.username}"