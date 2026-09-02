from app.services.stats import getStudents
from app.models.students import Group
from app.extensions import db

from app.services.stats import getStudents
from app.models.students import Group
from app.extensions import db

import random

def assign_students_to_groups(session, group_names):
    """
    If NEW groups are created:
        Reassigns ALL students across all groups for equal gender distribution.
    If ONLY EXISTING groups are targeted:
        Assigns ONLY unassigned students to the smallest existing groups.
    Students are randomly shuffled before placement.
    """
    if not group_names:
        return []

    # 1. Fetch all students for current session
    all_students = getStudents(session, paginate=False)

    # 2. Check existing vs new groups
    existing_groups = Group.query.filter(Group.name.in_(group_names)).all()
    existing_names = {g.name for g in existing_groups}

    new_names = [name for name in group_names if name not in existing_names]

    # Create genuinely new group models
    new_groups = [Group(name=name) for name in new_names]
    if new_groups:
        db.session.add_all(new_groups)
        db.session.flush()

    all_target_groups = existing_groups + new_groups

    # 3. Determine student pool to distribute
    if new_groups:
        students_to_assign = all_students
    else:
        students_to_assign = [s for s in all_students if not s.hasGroup()]

    if not students_to_assign:
        db.session.commit()
        return all_target_groups

    # 4. Initialize tracker dictionaries
    group_sizes = {g: 0 for g in all_target_groups}
    female_counts = {g: 0 for g in all_target_groups}

    if not new_groups:
        for g in all_target_groups:
            existing_members = getattr(g, 'students', []) or []
            group_sizes[g] = len(existing_members)
            female_counts[g] = sum(
                1 for s in existing_members 
                if str(s.getGender()).lower() in ("female", "f")
            )
    else:
        # Clear existing group associations in memory when reassigning everyone
        for s in students_to_assign:
            s.group = None
            s.group_id = None

    # 5. Categorize students by gender
    females = [s for s in students_to_assign if str(s.getGender()).lower() in ("female", "f")]
    males = [s for s in students_to_assign if str(s.getGender()).lower() in ("male", "m")]
    others = [s for s in students_to_assign if s not in females and s not in males]

    # --- RANDOMIZATION STEP ---
    # Shuffle each list in place to ensure random student assignment
    random.shuffle(females)
    random.shuffle(males)
    random.shuffle(others)

    # Helper function to place student into target group
    def assign_to_group(student, group):
        student.group = group
        if hasattr(student, 'setGroup'):
            student.setGroup()
        group_sizes[group] += 1

    # 6A. Distribute FEMALES randomly across 0-female groups first
    for student in females:
        target_group = min(
            all_target_groups,
            key=lambda g: (female_counts[g], group_sizes[g])
        )
        assign_to_group(student, target_group)
        female_counts[target_group] += 1

    # 6B. Distribute MALES & OTHERS randomly to balance overall group sizes
    for student in males + others:
        target_group = min(all_target_groups, key=lambda g: group_sizes[g])
        assign_to_group(student, target_group)

    # 7. Commit changes to database
    db.session.commit()

    return all_target_groups