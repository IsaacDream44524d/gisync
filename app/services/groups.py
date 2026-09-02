from app.models.students import Group, Student
from app.extensions import db
from sqlalchemy import select

def delete_all_groups(session=None):
    """Deletes all groups that have students in the given session (or all groups if no session specified)."""
    stmt = select(Group)
    
    if session:
        # Join through students to filter groups tied to this session
        stmt = stmt.join(Group.students).where(Student.session == session).distinct()
        
    groups = db.session.scalars(stmt).all()
    
    for group in groups:
        # Unassign students
        if hasattr(group, 'students') and group.students:
            for student in list(group.students):
                student.group_id = None
                if hasattr(student, 'clearGroup'):
                    student.clearGroup()
        
        db.session.delete(group)
        
    db.session.commit()
    return len(groups)


def cleanup_empty_groups(session=None):
    """Finds and deletes any group that has 0 students assigned."""
    # Select all groups using modern SQLAlchemy 2.0 syntax
    stmt = select(Group)
    all_groups = db.session.scalars(stmt).all()
    deleted_count = 0

    for group in all_groups:
        student_count = len(group.students) if hasattr(group, 'students') and group.students else 0
        if student_count == 0:
            db.session.delete(group)
            deleted_count += 1

    if deleted_count > 0:
        db.session.commit()

    return deleted_count