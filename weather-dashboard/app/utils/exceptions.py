"""Custom exceptions for weather application"""


class WeatherAPIException(Exception):
    """Base exception for weather API errors"""
    pass


class CityNotFound(WeatherAPIException):
    """Raised when city is not found"""
    pass


class InvalidCityName(WeatherAPIException):
    """Raised when city name is invalid"""
    pass


class APIKeyMissing(WeatherAPIException):
    """Raised when API key is not configured"""
    pass


class APILimitExceeded(WeatherAPIException):
    """Raised when API rate limit is exceeded"""
    pass


class NetworkError(WeatherAPIException):
    """Raised when network request fails"""
    pass


class InvalidUnits(WeatherAPIException):
    """Raised when invalid units are provided"""
    pass
