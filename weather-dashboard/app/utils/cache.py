"""Cache utilities for weather application"""

from app import cache
from functools import wraps


def cache_weather(timeout=None):
    """
    Decorator to cache weather API responses
    
    Args:
        timeout: Cache timeout in seconds
    
    Returns:
        Decorated function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f'weather_{f.__name__}_{str(args)}_{str(kwargs)}'
            
            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Call original function
            result = f(*args, **kwargs)
            
            # Store in cache
            cache.set(cache_key, result, timeout=timeout)
            
            return result
        return decorated_function
    return decorator


def clear_weather_cache():
    """
    Clear all weather-related cache entries
    """
    cache.clear()
