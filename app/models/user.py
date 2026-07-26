from app.extensions import db
from datetime import datetime, timezone
from app.extensions import login_manager, bcrypt
from flask_login import UserMixin
import enum

# responsible for session management
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class UserRole(enum.Enum):
    STUDENT = 'student'
    ADMIN = 'admin'
    SUPER_ADMIN = 'super_admin'


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(25), nullable=False, unique=True, index=True)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False, index=True)
    year = db.Column(db.Integer, nullable=False, default=2, index=True)
    role = db.Column(db.Enum(UserRole), default=UserRole.STUDENT, nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)



    def hasRole(self, role_name):
        return any(self.role == role_name)

    def iAdmin(self):
        return self.has_role('admin') or self.has_role('super_admin')

    def isSuperAdmin(self):
        return self.has_role('super_admin')

    def setPassword(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


    def __repr__(self):
        return f"<User {self.username} ({self.role.value})"