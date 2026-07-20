from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app import db
from app.models.student import Student
from app.schemas.student_schema import StudentSchema, StudentUpdateSchema
from app.utils.validators import (
    validate_student_data,
    validate_update_data,
    validate_pagination,
    ValidationError
)

students_bp = Blueprint('students', __name__, url_prefix='/students')

student_schema = StudentSchema()
student_list_schema = StudentSchema(many=True)
student_update_schema = StudentUpdateSchema()


@students_bp.route('', methods=['GET'])
def get_all_students():
    """
    Get all students with pagination support
    
    Query Parameters:
        page: Page number (default: 1)
        per_page: Items per page (default: 10, max: 100)
    
    Returns:
        JSON list of students with pagination metadata
    """
    try:
        page = request.args.get('page', 1)
        per_page = request.args.get('per_page', 10)
        
        # Validate pagination parameters
        page, per_page = validate_pagination(page, per_page)
        
        # Paginate results
        pagination = Student.query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'success': True,
            'data': student_list_schema.dump(pagination.items),
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        }, 200
    
    except ValidationError as e:
        return {'success': False, 'error': str(e)}, 400
    except Exception as e:
        print(f'Error in get_all_students: {str(e)}')
        return {'success': False, 'error': 'Internal server error'}, 500


@students_bp.route('/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """
    Get a specific student by ID
    
    Args:
        student_id: Student ID
    
    Returns:
        JSON object of the student
    """
    try:
        # Validate student ID
        from app.utils.validators import validate_student_id
        student_id = validate_student_id(student_id)
        
        student = Student.query.get(student_id)
        if not student:
            return {'success': False, 'error': 'Student not found'}, 404
        
        return {'success': True, 'data': student_schema.dump(student)}, 200
    
    except ValidationError as e:
        return {'success': False, 'error': str(e)}, 400
    except Exception as e:
        print(f'Error in get_student: {str(e)}')
        return {'success': False, 'error': 'Internal server error'}, 500


@students_bp.route('', methods=['POST'])
def create_student():
    """
    Create a new student
    
    Request Body:
        {
            "name": "John Doe",
            "department": "Computer Science",
            "cgpa": 3.8,
            "email": "john@example.com"
        }
    
    Returns:
        Created student object with 201 status
    """
    try:
        data = request.get_json()
        
        # Validate data
        validate_student_data(data)
        
        # Check for duplicate email
        existing_email = Student.query.filter_by(email=data['email']).first()
        if existing_email:
            return {'success': False, 'error': 'Email already exists'}, 409
        
        # Create student
        student = Student(
            name=data['name'].strip(),
            department=data['department'].strip(),
            cgpa=float(data['cgpa']),
            email=data['email'].strip()
        )
        db.session.add(student)
        db.session.commit()
        
        return {'success': True, 'data': student_schema.dump(student)}, 201
    
    except ValidationError as e:
        return {'success': False, 'error': str(e)}, 400
    except IntegrityError as e:
        db.session.rollback()
        return {'success': False, 'error': 'Email already exists'}, 409
    except Exception as e:
        db.session.rollback()
        print(f'Error in create_student: {str(e)}')
        return {'success': False, 'error': 'Internal server error'}, 500


@students_bp.route('/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """
    Update a student record
    
    Args:
        student_id: Student ID
    
    Request Body:
        {
            "name": "Jane Doe",
            "department": "Data Science",
            "cgpa": 3.9,
            "email": "jane@example.com"
        }
    
    Returns:
        Updated student object
    """
    try:
        from app.utils.validators import validate_student_id
        student_id = validate_student_id(student_id)
        
        student = Student.query.get(student_id)
        if not student:
            return {'success': False, 'error': 'Student not found'}, 404
        
        data = request.get_json()
        
        # Validate update data
        validate_update_data(data)
        
        # Check for duplicate email if being updated
        if 'email' in data and data['email'] and data['email'].strip() != student.email:
            existing = Student.query.filter_by(email=data['email'].strip()).first()
            if existing:
                return {'success': False, 'error': 'Email already exists'}, 409
        
        # Update student fields
        if 'name' in data and data['name'] is not None:
            student.name = data['name'].strip()
        if 'department' in data and data['department'] is not None:
            student.department = data['department'].strip()
        if 'cgpa' in data and data['cgpa'] is not None:
            student.cgpa = float(data['cgpa'])
        if 'email' in data and data['email'] is not None:
            student.email = data['email'].strip()
        
        db.session.commit()
        return {'success': True, 'data': student_schema.dump(student)}, 200
    
    except ValidationError as e:
        return {'success': False, 'error': str(e)}, 400
    except IntegrityError as e:
        db.session.rollback()
        return {'success': False, 'error': 'Email already exists'}, 409
    except Exception as e:
        db.session.rollback()
        print(f'Error in update_student: {str(e)}')
        return {'success': False, 'error': 'Internal server error'}, 500


@students_bp.route('/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """
    Delete a student record
    
    Args:
        student_id: Student ID
    
    Returns:
        Success message with 204 status
    """
    try:
        from app.utils.validators import validate_student_id
        student_id = validate_student_id(student_id)
        
        student = Student.query.get(student_id)
        if not student:
            return {'success': False, 'error': 'Student not found'}, 404
        
        db.session.delete(student)
        db.session.commit()
        return {'success': True, 'message': 'Student deleted successfully'}, 204
    
    except ValidationError as e:
        return {'success': False, 'error': str(e)}, 400
    except Exception as e:
        db.session.rollback()
        print(f'Error in delete_student: {str(e)}')
        return {'success': False, 'error': 'Internal server error'}, 500
