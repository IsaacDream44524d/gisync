from app.models import User
from app.models.enums import UserRole
from app.extensions import db

class PermissionError(Exception):
    pass

def roleChangeError(user: User, target: User, role: UserRole):
    try:
        new_role = UserRole(role.lower())

    except ValueError:
        raise PermissionError(f"Invalid Role: '{role}'")

    
    # only super_admin can change user roles
    if user.role != UserRole.SUPER_ADMIN:
        raise PermissionError('Request Denied')

    # one can not change their own role
    if user.id == target.id:
        raise PermissionError('You cannot change your own role')

    current_super_admin = User.query.filter(User.role == UserRole.SUPER_ADMIN, User.id != target.id).count()

    current_admin = User.query.filter(User.role == UserRole.ADMIN, User.id != target.id).count()

    if new_role == UserRole.SUPER_ADMIN and current_super_admin >= 1:
        raise PermissionError('There can only be one super_admin')

    if new_role == UserRole.ADMIN and current_admin >= 2:
        raise PermissionError('There can only be two admins')

    if (target.role == UserRole.SUPER_ADMIN and new_role != UserRole.SUPER_ADMIN and current_super_admin == 0):
        raise PermissionError('Cannot demote the only super_admin')
    
    
    target.role = new_role
    db.session.commit()
    return target

