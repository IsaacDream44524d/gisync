import enum

class UserRole(enum.Enum):
    STUDENT = 'student'
    ADMIN = 'admin'
    SUPER_ADMIN = 'super_admin'


class ReportStatus(enum.Enum):
    PENDING = 'pending'
    RESOLVED = 'resolved'
    DISMISSES = 'dismissed'


class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"