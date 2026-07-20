from datetime import datetime
from app import db


class Student(db.Model):
    """
    Student model representing a student record in the database
    """
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    cgpa = db.Column(db.Float, default=0.0, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Student {self.id}: {self.name}>'
    
    def to_dict(self):
        """
        Convert student object to dictionary
        
        Returns:
            Dictionary representation of the student
        """
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'cgpa': self.cgpa,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
