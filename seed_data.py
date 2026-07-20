"""
Sample data initialization script for Student Management System
Run this script to populate the database with sample student records
"""

from app import create_app, db
from app.models.student import Student


def create_sample_data():
    """
    Create and insert sample student data into the database
    """
    app = create_app('development')
    
    with app.app_context():
        # Clear existing data
        db.session.query(Student).delete()
        db.session.commit()
        
        # Sample student data
        sample_students = [
            Student(
                name='Alice Johnson',
                department='Computer Science',
                cgpa=3.9,
                email='alice.johnson@student.edu'
            ),
            Student(
                name='Bob Smith',
                department='Computer Science',
                cgpa=3.7,
                email='bob.smith@student.edu'
            ),
            Student(
                name='Carol White',
                department='Data Science',
                cgpa=3.85,
                email='carol.white@student.edu'
            ),
            Student(
                name='David Brown',
                department='Electrical Engineering',
                cgpa=3.6,
                email='david.brown@student.edu'
            ),
            Student(
                name='Eve Davis',
                department='Data Science',
                cgpa=3.95,
                email='eve.davis@student.edu'
            ),
            Student(
                name='Frank Miller',
                department='Mechanical Engineering',
                cgpa=3.5,
                email='frank.miller@student.edu'
            ),
            Student(
                name='Grace Lee',
                department='Computer Science',
                cgpa=3.92,
                email='grace.lee@student.edu'
            ),
            Student(
                name='Henry Taylor',
                department='Civil Engineering',
                cgpa=3.4,
                email='henry.taylor@student.edu'
            ),
            Student(
                name='Iris Martinez',
                department='Data Science',
                cgpa=3.88,
                email='iris.martinez@student.edu'
            ),
            Student(
                name='Jack Wilson',
                department='Computer Science',
                cgpa=3.75,
                email='jack.wilson@student.edu'
            ),
            Student(
                name='Karen Anderson',
                department='Electrical Engineering',
                cgpa=3.65,
                email='karen.anderson@student.edu'
            ),
            Student(
                name='Leo Thompson',
                department='Mechanical Engineering',
                cgpa=3.55,
                email='leo.thompson@student.edu'
            ),
        ]
        
        # Add all students to session
        db.session.add_all(sample_students)
        
        try:
            # Commit the transaction
            db.session.commit()
            print(f'✓ Successfully created {len(sample_students)} sample students')
            
            # Display created students
            print('\nSample Students Created:')
            print('-' * 90)
            print(f'{'ID':^4} | {'Name':^20} | {'Department':^22} | {'CGPA':^6} | {'Email':^30}')
            print('-' * 90)
            for student in sample_students:
                print(f'{student.id:^4} | {student.name:^20} | {student.department:^22} | {student.cgpa:^6.2f} | {student.email:^30}')
            print('-' * 90)
            
        except Exception as e:
            db.session.rollback()
            print(f'✗ Error creating sample data: {str(e)}')
            raise


if __name__ == '__main__':
    create_sample_data()
