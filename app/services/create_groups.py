from sqlalchemy import select
from app.services.stats import getStudents
from app.models.students import Group
from app.extensions import db



def auto_assign_groups(session, group_names):
    students = getStudents(db.session)

    females = [
        females for females in students
        if females.gender.value.lower() == "female"
    ]

    males = [
        males for males in students
        if males.gender.value.lower() == "male"
    ]

    groups = []

    # Create groups
    for name in group_names:
        group = Group(name=name)
        session.add(group)
        groups.append(group)

    session.flush()

    # Spread females first
    group_index = 0
    for student in females:
        student.group = groups[group_index]
        group_index = (group_index + 1) % len(groups)

    # Spread males next
    for student in males:
        student.group = groups[group_index]
        group_index = (group_index + 1) % len(groups)

    session.commit()

    return groups