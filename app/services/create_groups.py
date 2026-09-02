from app.services.stats import getStudents
from app.models.students import Group
from app.extensions import db

from app.services.stats import getStudents
from app.models.students import Group
from app.extensions import db

import random

import random

def assign_students_to_groups(session, group_names):
    """
    If new groups are created:
        Reassign ALL students across all groups.

    If only existing groups are used:
        Assign ONLY unassigned students.

    Rules:
        - Every group gets one female first (if enough females exist).
        - Remaining females are distributed evenly.
        - Males and others are distributed to balance group sizes.
    """

    if not group_names:
        return []

    # Get all students
    all_students = getStudents(session, paginate=False)

    # Find existing groups
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

    all_target_groups = existing_groups + new_groups

    # Determine student pool
    if new_groups:
        students_to_assign = all_students

        # Clear existing assignments
        for student in students_to_assign:
            student.group = None
            student.group_id = None

            if hasattr(student, "setGroup"):
                student.setGroup(False)

    else:
        students_to_assign = [
            s for s in all_students
            if not s.hasGroup()
        ]

    if not students_to_assign:
        session.commit()
        return all_target_groups

    # Track group sizes and female counts
    group_sizes = {}
    female_counts = {}

    for group in all_target_groups:

        if new_groups:
            group_sizes[group] = 0
            female_counts[group] = 0

        else:
            members = list(group.students or [])

            group_sizes[group] = len(members)

            female_counts[group] = sum(
                1
                for s in members
                if str(s.getGender()).lower() in ("female", "f")
            )

    # Split by gender
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

    # Randomize
    random.shuffle(females)
    random.shuffle(males)
    random.shuffle(others)

    def assign_to_group(student, group):
        student.group = group

        if hasattr(student, "setGroup"):
            student.setGroup(True)

        group_sizes[group] += 1

    # ---------------------------------------------------------
    # PASS 1:
    # Ensure each group gets one female if possible
    # ---------------------------------------------------------

    groups_needing_female = [
        g for g in all_target_groups
        if female_counts[g] == 0
    ]

    for group in groups_needing_female:
        if not females:
            break

        student = females.pop()

        assign_to_group(student, group)
        female_counts[group] += 1

    # ---------------------------------------------------------
    # PASS 2:
    # Distribute remaining females evenly
    # ---------------------------------------------------------

    for student in females:

        target_group = min(
            all_target_groups,
            key=lambda g: (
                female_counts[g],
                group_sizes[g]
            )
        )

        assign_to_group(student, target_group)
        female_counts[target_group] += 1

    # ---------------------------------------------------------
    # PASS 3:
    # Distribute males and others evenly
    # ---------------------------------------------------------

    for student in males + others:

        target_group = min(
            all_target_groups,
            key=lambda g: group_sizes[g]
        )

        assign_to_group(student, target_group)

    session.commit()

    return all_target_groups