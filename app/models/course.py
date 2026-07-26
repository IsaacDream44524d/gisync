from app.extensions import db

class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True, index=True)
    code = db.Column(db.String(25), nullable=False, unique=True, index=True)
    name = db.Column(db.String(255), nullable=False, unique=True, index=True)
   

    def __repr__(self):
        return f"<Course {self.id} ({self.code}, {self.name})"

    