from datetime import date
import re


class ValidationError(Exception):
    """Custom validation error"""
    pass


def validate_email(email):
    """
    Validate email format
    
    Args:
        email: Email string to validate
    
    Returns:
        Boolean indicating if email is valid
    """
    if not email:
        raise ValidationError('Email is required')
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, str(email).strip()):
        raise ValidationError('Invalid email format. Please use a valid email address.')
    
    return True


def validate_name(name):
    """
    Validate student name
    
    Args:
        name: Name string to validate
    
    Returns:
        Boolean indicating if name is valid
    """
    if not name:
        raise ValidationError('Name is required')
    
    name = str(name).strip()
    
    if len(name) < 2:
        raise ValidationError('Name must be at least 2 characters long')
    
    if len(name) > 100:
        raise ValidationError('Name must not exceed 100 characters')
    
    if not re.match(r'^[a-zA-Z\s\'-]+$', name):
        raise ValidationError('Name can only contain letters, spaces, hyphens, and apostrophes')
    
    return True


def validate_department(department):
    """
    Validate department name
    
    Args:
        department: Department string to validate
    
    Returns:
        Boolean indicating if department is valid
    """
    if not department:
        raise ValidationError('Department is required')
    
    department = str(department).strip()
    
    if len(department) < 2:
        raise ValidationError('Department must be at least 2 characters long')
    
    if len(department) > 100:
        raise ValidationError('Department must not exceed 100 characters')
    
    return True


def validate_cgpa(cgpa):
    """
    Validate CGPA value
    
    Args:
        cgpa: CGPA value to validate
    
    Returns:
        Boolean indicating if CGPA is valid (0.0 to 4.0)
    """
    if cgpa is None:
        raise ValidationError('CGPA is required')
    
    try:
        cgpa_float = float(cgpa)
    except (ValueError, TypeError):
        raise ValidationError('CGPA must be a valid number')
    
    if cgpa_float < 0.0:
        raise ValidationError('CGPA cannot be negative')
    
    if cgpa_float > 4.0:
        raise ValidationError('CGPA cannot exceed 4.0')
    
    return True


def validate_student_data(data):
    """
    Validate complete student data for creation
    
    Args:
        data: Dictionary with student data
    
    Returns:
        Boolean indicating if data is valid
    
    Raises:
        ValidationError with error messages
    """
    if not data:
        raise ValidationError('Request body cannot be empty')
    
    if not isinstance(data, dict):
        raise ValidationError('Request body must be a JSON object')
    
    # Validate required fields
    required_fields = ['name', 'department', 'cgpa', 'email']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        raise ValidationError(f'Missing required fields: {", ".join(missing_fields)}')
    
    # Validate individual fields
    validate_name(data['name'])
    validate_department(data['department'])
    validate_cgpa(data['cgpa'])
    validate_email(data['email'])
    
    return True


def validate_update_data(data):
    """
    Validate student update data (partial updates allowed)
    
    Args:
        data: Dictionary with student data to update
    
    Returns:
        Boolean indicating if data is valid
    
    Raises:
        ValidationError with error messages
    """
    if not data:
        raise ValidationError('Request body cannot be empty')
    
    if not isinstance(data, dict):
        raise ValidationError('Request body must be a JSON object')
    
    # Validate individual fields if provided
    if 'name' in data and data['name'] is not None:
        validate_name(data['name'])
    
    if 'department' in data and data['department'] is not None:
        validate_department(data['department'])
    
    if 'cgpa' in data and data['cgpa'] is not None:
        validate_cgpa(data['cgpa'])
    
    if 'email' in data and data['email'] is not None:
        validate_email(data['email'])
    
    return True


def validate_pagination(page, per_page):
    """
    Validate pagination parameters
    
    Args:
        page: Page number
        per_page: Items per page
    
    Returns:
        Tuple (page, per_page) with validated values
    
    Raises:
        ValidationError with error messages
    """
    try:
        page = int(page) if page else 1
        per_page = int(per_page) if per_page else 10
    except (ValueError, TypeError):
        raise ValidationError('Page and per_page must be integers')
    
    if page < 1:
        raise ValidationError('Page number must be greater than 0')
    
    if per_page < 1:
        raise ValidationError('Items per page must be greater than 0')
    
    if per_page > 100:
        per_page = 100
    
    return page, per_page


def validate_student_id(student_id):
    """
    Validate student ID
    
    Args:
        student_id: Student ID to validate
    
    Returns:
        Integer student ID
    
    Raises:
        ValidationError with error messages
    """
    try:
        student_id = int(student_id)
    except (ValueError, TypeError):
        raise ValidationError('Student ID must be a valid integer')
    
    if student_id < 1:
        raise ValidationError('Student ID must be greater than 0')
    
    return student_id
