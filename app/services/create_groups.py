from app.services.stats import getStudents
from app.models.students import Group
from app.extensions import db

from app.services.stats import getStudents
from app.models.students import Group
from app.extensions import db


def assign_students_to_groups(session, group_names):
    """
    If NEW groups are created:
        Reassigns ALL students across all groups for equal gender distribution.
    If ONLY EXISTING groups are targeted:
        Assigns ONLY unassigned students to the smallest existing groups.
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
    # If new groups were created -> reassign EVERYONE to achieve equal distribution
    # If no new groups were created -> assign ONLY unassigned students
    if new_groups:
        students_to_assign = all_students
    else:
        students_to_assign = [s for s in all_students if not s.hasGroup()]

    if not students_to_assign:
        db.session.commit()
        return all_target_groups

    # 4. Initialize group sizes
    # If reassigning everyone, start all sizes at 0. Otherwise, count current members.
    group_sizes = {}
    for g in all_target_groups:
        if new_groups:
            group_sizes[g] = 0
        else:
            current_count = len(g.students) if hasattr(g, 'students') and g.students else 0
            group_sizes[g] = current_count

    # 5. Categorize students by gender
    females = [s for s in students_to_assign if str(s.getGender()).lower() in ("female", "f")]
    males = [s for s in students_to_assign if str(s.getGender()).lower() in ("male", "m")]
    others = [s for s in students_to_assign if s not in females and s not in males]

    # Helper function to place student into the smallest group
    def assign_student(student):
        smallest_group = min(all_target_groups, key=lambda g: group_sizes[g])
        
        student.group = smallest_group
        if hasattr(student, 'setGroup'):
            student.setGroup()

        group_sizes[smallest_group] += 1

    # 6. Distribute females, then males, then others
    for student in females:
        assign_student(student)

    for student in males:
        assign_student(student)

    for student in others:
        assign_student(student)

    # 7. Commit changes to database
    db.session.commit()

    return all_target_groups