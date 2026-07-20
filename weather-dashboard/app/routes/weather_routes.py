"""Weather API routes"""

from flask import Blueprint, request, jsonify
from app.services.weather_service import WeatherService
from app.utils.exceptions import WeatherAPIException
from app.utils.validators import validate_city_name, validate_units, validate_days

weather_bp = Blueprint('weather', __name__)
weather_service = WeatherService()


@weather_bp.route('/current', methods=['GET'])
def get_current_weather():
    """
    Get current weather for a city
    
    Query Parameters:
        city (required): City name
        units (optional): 'metric', 'imperial', or 'kelvin'
    
    Returns:
        JSON response with current weather data
    """
    try:
        city = request.args.get('city', '').strip()
        units = request.args.get('units', 'metric')
        
        # Validate inputs
        validate_city_name(city)
        units = validate_units(units)
        
        # Get weather data
        weather = weather_service.get_current_weather(city, units)
        
        return {
            'success': True,
            'data': weather.to_dict()
        }, 200
    
    except WeatherAPIException as e:
        return {'success': False, 'error': str(e)}, 400
    except Exception as e:
        print(f'Error in get_current_weather: {str(e)}')
        return {'success': False, 'error': 'Internal server error'}, 500


@weather_bp.route('/forecast', methods=['GET'])
def get_forecast():
    """
    Get weather forecast for a city
    
    Query Parameters:
        city (required): City name
        units (optional): 'metric', 'imperial', or 'kelvin'
        days (optional): Number of days (1-5)
    
    Returns:
        JSON response with forecast data
    """
    try:
        city = request.args.get('city', '').strip()
        units = request.args.get('units', 'metric')
        days = request.args.get('days', '5')
        
        # Validate inputs
        validate_city_name(city)
        units = validate_units(units)
        days = validate_days(days)
        
        # Get forecast data
        forecast = weather_service.get_forecast(city, units)
        forecast_data = forecast.to_list()[:days]
        
        return {
            'success': True,
            'data': {
                'city': weather_service.get_city_name(city),
                'units': units,
                'forecast': forecast_data
            }
        }, 200
    
    except WeatherAPIException as e:
        return {'success': False, 'error': str(e)}, 400
    except ValueError as e:
        return {'success': False, 'error': str(e)}, 400
    except Exception as e:
        print(f'Error in get_forecast: {str(e)}')
        return {'success': False, 'error': 'Internal server error'}, 500


@weather_bp.route('/search', methods=['GET'])
def search_cities():
    """
    Search for cities
    
    Query Parameters:
        query (required): Partial city name
    
    Returns:
        JSON response with matching cities
    """
    try:
        query = request.args.get('query', '').strip()
        
        if len(query) < 2:
            return {'success': False, 'error': 'Search query must be at least 2 characters'}, 400
        
        # Search for cities
        cities = weather_service.search_cities(query)
        
        return {
            'success': True,
            'data': cities
        }, 200
    
    except WeatherAPIException as e:
        return {'success': False, 'error': str(e)}, 400
    except Exception as e:
        print(f'Error in search_cities: {str(e)}')
        return {'success': False, 'error': 'Internal server error'}, 500


@weather_bp.route('/convert', methods=['POST'])
def convert_temperature():
    """
    Convert temperature between units
    
    JSON Body:
        {
            "temperature": 20,
            "from_units": "celsius",
            "to_units": "fahrenheit"
        }
    
    Returns:
        JSON response with converted temperature
    """
    try:
        data = request.get_json()
        
        if not data:
            return {'success': False, 'error': 'Request body is required'}, 400
        
        temperature = float(data.get('temperature'))
        from_units = data.get('from_units', 'celsius').lower()
        to_units = data.get('to_units', 'fahrenheit').lower()
        
        # Convert temperature
        converted = weather_service.convert_temperature(
            temperature, from_units, to_units
        )
        
        return {
            'success': True,
            'data': {
                'original': temperature,
                'from_units': from_units,
                'converted': converted,
                'to_units': to_units
            }
        }, 200
    
    except (ValueError, KeyError) as e:
        return {'success': False, 'error': str(e)}, 400
    except Exception as e:
        print(f'Error in convert_temperature: {str(e)}')
        return {'success': False, 'error': 'Internal server error'}, 500
