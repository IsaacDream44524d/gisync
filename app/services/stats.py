from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.extensions import cache
from flask import request
from app.extensions import db

from app.models.user import User
from app.models.students import Student
from app.models.file import File
from app.models.downloadLog import DownloadLog
from app.models.course import Course
from app.models.schedule import Schedule
from app.models.enums import UserRole

def getAdminStats(session: Session) -> dict:
    #get stats for admin dashboard and cache for 60s so concurrent request dont hit db at once
    try:
        cached = cache.get('admin_stats')

    except Exception:
        cached = None

    if cached is not None:
        return cached

    stats = {
        'total_files': session.query(func.count(File.id)).scalar() or 0,
        'total_students': (session.query(func.count(User.id)).filter(User.role == UserRole.STUDENT).scalar() or 0),
        'total_admin': (session.query(func.count(User.id)).filter(User.role == UserRole.ADMIN).scalar() or 0),
        'total_downloads': session.query(func.count(DownloadLog.id)).scalar() or 0,
        'total_modules': session.query(func.count(Course.id)).scalar() or 0,
        'total_schedules': session.query(func.count(Schedule.id)).scalar() or 0,
        'pending_invites': session.query(func.count(User.id).filter(User.is_active == False)).scalar() or 0
    }

    try:
        cache.set('admin_stats', stats, timeout=60) #TTL = 60s

    except Exception:
        pass

    return stats

def getStudentStats(session: Session, userId: int) -> dict:
    return {
        'student_downloads': (session.query(func.count(DownloadLog.id)).filter(DownloadLog.downloaded_by == userId).scalar() or 0),
        'total_files': session.query(func.count(File.id)).scalar or 0,
        'total_modules': session.query(func.count(Course.id)).scalar() or 0,
        #add stats for number of classes that day
    }

def getAllStudents(session: Session, select: select) -> dict:
    return session.scalars(select(User).order_by(User.created_at.desc())).all()

from sqlalchemy.orm import joinedload

def getStudents(session: Session):
    page = request.args.get("page", 1, type=int)

    return db.paginate(
        select(Student).order_by(Student.created_at.desc()),
        page=page,
        per_page=10
    )

