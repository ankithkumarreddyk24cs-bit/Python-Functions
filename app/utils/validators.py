from datetime import date
import re


def validate_email(email):
    """
    Validate email format
    
    Args:
        email: Email string to validate
    
    Returns:
        Boolean indicating if email is valid
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_cgpa(cgpa):
    """
    Validate CGPA value
    
    Args:
        cgpa: CGPA value to validate
    
    Returns:
        Boolean indicating if CGPA is valid (0.0 to 4.0)
    """
    try:
        cgpa_float = float(cgpa)
        return 0.0 <= cgpa_float <= 4.0
    except (ValueError, TypeError):
        return False


def validate_student_data(data):
    """
    Validate complete student data
    
    Args:
        data: Dictionary with student data
    
    Returns:
        Tuple (is_valid, error_messages)
    """
    errors = []
    
    if 'email' in data and not validate_email(data['email']):
        errors.append('Invalid email format')
    
    if 'cgpa' in data and data['cgpa'] is not None and not validate_cgpa(data['cgpa']):
        errors.append('CGPA must be between 0.0 and 4.0')
    
    return len(errors) == 0, errors
