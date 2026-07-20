"""Validators for weather application"""

import re
from app.utils.exceptions import InvalidCityName, InvalidUnits


def validate_city_name(city):
    """
    Validate city name
    
    Args:
        city: City name to validate
    
    Returns:
        Boolean indicating if city name is valid
    
    Raises:
        InvalidCityName if validation fails
    """
    if not city:
        raise InvalidCityName('City name is required')
    
    city = str(city).strip()
    
    if len(city) < 2:
        raise InvalidCityName('City name must be at least 2 characters')
    
    if len(city) > 100:
        raise InvalidCityName('City name must not exceed 100 characters')
    
    # Allow letters, spaces, hyphens, and apostrophes
    if not re.match(r"^[a-zA-Z\s\'-]+$", city):
        raise InvalidCityName('City name contains invalid characters')
    
    return True


def validate_units(units):
    """
    Validate temperature units
    
    Args:
        units: Temperature units ('metric', 'imperial', or 'kelvin')
    
    Returns:
        Validated units string
    
    Raises:
        InvalidUnits if validation fails
    """
    valid_units = ['metric', 'imperial', 'kelvin']
    
    if units and units not in valid_units:
        raise InvalidUnits(f'Invalid units. Must be one of: {valid_units}')
    
    return units or 'metric'


def validate_days(days):
    """
    Validate forecast days
    
    Args:
        days: Number of days for forecast
    
    Returns:
        Validated days integer
    
    Raises:
        ValueError if validation fails
    """
    try:
        days = int(days) if days else 5
    except (ValueError, TypeError):
        raise ValueError('Days must be an integer')
    
    if days < 1 or days > 5:
        raise ValueError('Days must be between 1 and 5')
    
    return days
