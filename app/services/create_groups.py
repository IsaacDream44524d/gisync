from app.services.stats import getStudents
from app.models.students import Group
from app.extensions import db

from app.services.stats import getStudents
from app.models.students import Group
from app.extensions import db

import random

import random

import random

def assign_students_to_groups(session, group_names):
    if not group_names:
        return []

    # Get all students
    all_students = getStudents(session, paginate=False)

    # Get existing groups
    existing_groups = Group.query.filter(
        Group.name.in_(group_names)
    ).all()

    existing_names = {g.name for g in existing_groups}

    # Create missing groups
    new_groups = [
        Group(name=name)
        for name in group_names
        if name not in existing_names
    ]

    if new_groups:
        session.add_all(new_groups)
        session.flush()

    groups = existing_groups + new_groups

    # --------------------------------------------------
    # FULL REDISTRIBUTION IF NEW GROUPS CREATED
    # --------------------------------------------------

    if new_groups:
        students_to_assign = all_students

        for student in students_to_assign:
            student.group = None
            student.group_id = None

            if hasattr(student, "setGroup"):
                student.setGroup(False)

        session.flush()

        group_sizes = {g: 0 for g in groups}
        female_counts = {g: 0 for g in groups}

    else:
        students_to_assign = [
            s for s in all_students
            if not s.hasGroup()
        ]

        group_sizes = {}
        female_counts = {}

        for group in groups:
            members = list(group.students or [])
            group_sizes[group] = len(members)
            female_counts[group] = sum(
                1 for s in members
                if str(s.getGender()).lower() in ("female", "f")
            )

    if not students_to_assign:
        session.commit()
        return groups

    # --------------------------------------------------
    # SPLIT BY GENDER & SHUFFLE
    # --------------------------------------------------

    females = [
        s for s in students_to_assign
        if str(s.getGender()).lower() in ("female", "f")
    ]

    males = [
        s for s in students_to_assign
        if str(s.getGender()).lower() in ("male", "m")
    ]

    others = [
        s for s in students_to_assign
        if str(s.getGender()).lower() not in ("female", "f", "male", "m")
    ]

    random.shuffle(females)
    random.shuffle(males)
    random.shuffle(others)

    def assign(student, group):
        student.group = group
        if hasattr(student, "setGroup"):
            student.setGroup(True)
        group_sizes[group] += 1

    # --------------------------------------------------
    # DISTRIBUTE FEMALES EVENLY (1 per group first)
    # --------------------------------------------------

    while females:
        student = females.pop()

        # Prioritize 0-female groups first (female_counts=0),
        # then break ties by choosing the smallest total group size
        target = min(
            groups,
            key=lambda g: (female_counts[g], group_sizes[g])
        )

        assign(student, target)
        female_counts[target] += 1

    # --------------------------------------------------
    # DISTRIBUTE MALES + OTHERS EVENLY
    # --------------------------------------------------

    remaining = males + others
    random.shuffle(remaining)

    for student in remaining:
        target = min(
            groups,
            key=lambda g: group_sizes[g]
        )
        assign(student, target)

    session.commit()

    return groups