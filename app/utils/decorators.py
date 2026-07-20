from functools import wraps
from flask import request
import traceback


def handle_errors(f):
    """
    Decorator to handle common errors in route handlers
    
    Returns:
        Decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return {'success': False, 'error': f'Invalid value: {str(e)}'}, 400
        except KeyError as e:
            return {'success': False, 'error': f'Missing required field: {str(e)}'}, 400
        except Exception as e:
            # Log the full traceback for debugging
            print(f'Error in {f.__name__}: {traceback.format_exc()}')
            return {'success': False, 'error': 'Internal server error'}, 500
    
    return decorated_function


def require_json(f):
    """
    Decorator to require JSON request body
    
    Returns:
        Decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return {'success': False, 'error': 'Request must be JSON'}, 400
        return f(*args, **kwargs)
    
    return decorated_function


def validate_request_data(schema):
    """
    Decorator to validate request data against a Marshmallow schema
    
    Args:
        schema: Marshmallow schema for validation
    
    Returns:
        Decorated function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            errors = schema.validate(data)
            if errors:
                return {'success': False, 'errors': errors}, 400
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator
