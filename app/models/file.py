from app.extensions import db
from datetime import datetime, timezone
from .course import Course
from .category import Category
from .user import User


class File(db.Model):
    __tablename__ = 'file'

    id = db.Column(db.Integer, primary_key=True, index=True)
    course_id = db.Column(db.Integer, db.ForeignKey(Course.id, ondelete='CASCADE') ,nullable=True, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id) ,nullable=False, index=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey(User.id) ,nullable=False, index=True)
    file_path = db.Column(db.String(500), nullable=False, unique=True)
    filename = db.Column(db.String(255), nullable=False, unique=True, index=True)
    file_size = db.Column(db.Integer, nullable=False) #stores as bytes
    is_deleted = db.Column(db.Boolean, default=False)
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    course = db.relationship('Course', backref=db.backref('files', lazy='dynamic'))
    category = db.relationship('Category', backref=db.backref('files', lazy='dynamic'))
    uploader = db.relationship('User', backref=db.backref('uploads', lazy='dynamic'))

    def __repr__(self):
            return f"<File {self.id} for course {self.course_id} and category {self.category_id} - deleted ={self.is_deleted})"