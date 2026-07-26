from app.extensions import db

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(255), nullable=False, unique=True, index=True)
   

    def __repr__(self):
        return f"<Course {self.id} ({self.name})"

    