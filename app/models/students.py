from app.extensions import db
from datetime import datetime, timezone
from flask_login import UserMixin
from .enums import UserRole, Gender





class Student(UserMixin, db.Model):
    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(25), nullable=False, unique=True, index=True)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)

    year = db.Column(db.Integer, nullable=False, default=2, index=True)
    gender = db.Column(db.Enum(Gender), nullable=False, index=True)
    has_group = db.Column(db.Boolean, default=False)

    role = db.Column(
        db.Enum(UserRole),
        default=UserRole.STUDENT,
        nullable=False,
        index=True
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True
    )

    group_id = db.Column(
        db.Integer,
        db.ForeignKey("group.id"),
        nullable=True
    )

    group = db.relationship(
        "Group",
        back_populates="students"
    )


class Group(db.Model):
    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True
    )

    students = db.relationship(
        "Student",
        back_populates="group",
        lazy=True
    )

    def __repr__(self):
        return f"<Group {self.name}>"