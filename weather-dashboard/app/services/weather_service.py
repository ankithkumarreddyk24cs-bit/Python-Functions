"""Weather service for API interactions"""

import requests
from flask import current_app
from app.utils.exceptions import (
    CityNotFound, APIKeyMissing, APILimitExceeded, NetworkError
)
from app.models.weather import Weather, Forecast
from app import cache


class WeatherService:
    """
    Service for interacting with OpenWeatherMap API
    """
    
    def __init__(self):
        self.api_key = None
        self.base_url = None
        self.timeout = 10
    
    def _get_config(self):
        """Get configuration from Flask app"""
        self.api_key = current_app.config.get('OPENWEATHERMAP_API_KEY')
        self.base_url = current_app.config.get('OPENWEATHERMAP_BASE_URL')
        self.timeout = current_app.config.get('WEATHER_API_TIMEOUT', 10)
        
        if not self.api_key:
            raise APIKeyMissing('OpenWeatherMap API key not configured')
    
    def get_current_weather(self, city, units='metric'):
        """
        Get current weather for a city
        
        Args:
            city: City name
            units: Temperature units
        
        Returns:
            Weather object
        
        Raises:
            CityNotFound if city is not found
        """
        self._get_config()
        
        # Check cache
        cache_key = f'weather_current_{city}_{units}'
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        try:
            url = f'{self.base_url}/weather'
            params = {
                'q': city,
                'units': units,
                'appid': self.api_key
            }
            
            response = requests.get(
                url,
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 404:
                raise CityNotFound(f'City "{city}" not found')
            elif response.status_code == 429:
                raise APILimitExceeded('API rate limit exceeded')
            elif response.status_code != 200:
                raise NetworkError(f'API returned status code {response.status_code}')
            
            data = response.json()
            weather = Weather(data, units)
            
            # Cache the result
            cache.set(cache_key, weather, timeout=600)
            
            return weather
        
        except requests.RequestException as e:
            raise NetworkError(f'Network error: {str(e)}')
    
    def get_forecast(self, city, units='metric', count=40):
        """
        Get weather forecast for a city
        
        Args:
            city: City name
            units: Temperature units
            count: Number of forecast items
        
        Returns:
            Forecast object
        
        Raises:
            CityNotFound if city is not found
        """
        self._get_config()
        
        # Check cache
        cache_key = f'weather_forecast_{city}_{units}'
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        try:
            url = f'{self.base_url}/forecast'
            params = {
                'q': city,
                'units': units,
                'cnt': count,
                'appid': self.api_key
            }
            
            response = requests.get(
                url,
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 404:
                raise CityNotFound(f'City "{city}" not found')
            elif response.status_code == 429:
                raise APILimitExceeded('API rate limit exceeded')
            elif response.status_code != 200:
                raise NetworkError(f'API returned status code {response.status_code}')
            
            data = response.json()
            forecast = Forecast(data.get('list', []), units)
            
            # Cache the result
            cache.set(cache_key, forecast, timeout=600)
            
            return forecast
        
        except requests.RequestException as e:
            raise NetworkError(f'Network error: {str(e)}')
    
    def search_cities(self, query):
        """
        Search for cities
        
        Args:
            query: City name query
        
        Returns:
            List of cities with coordinates
        """
        self._get_config()
        
        # Check cache
        cache_key = f'weather_search_{query}'
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        try:
            url = f'{self.base_url}/find'
            params = {
                'q': query,
                'type': 'like',
                'cnt': 10,
                'appid': self.api_key
            }
            
            response = requests.get(
                url,
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                raise NetworkError(f'API returned status code {response.status_code}')
            
            data = response.json()
            cities = []
            
            for item in data.get('list', []):
                city_info = {
                    'city': item.get('name'),
                    'country': item.get('sys', {}).get('country'),
                    'lat': item.get('coord', {}).get('lat'),
                    'lon': item.get('coord', {}).get('lon'),
                    'temperature': item.get('main', {}).get('temp')
                }
                cities.append(city_info)
            
            # Cache the result
            cache.set(cache_key, cities, timeout=1800)  # 30 minutes
            
            return cities
        
        except requests.RequestException as e:
            raise NetworkError(f'Network error: {str(e)}')
    
    def get_city_name(self, city):
        """
        Get formatted city name (for display)
        
        Args:
            city: City name
        
        Returns:
            Formatted city name
        """
        try:
            weather = self.get_current_weather(city)
            return f"{weather.city}, {weather.country}"
        except:
            return city
    
    @staticmethod
    def convert_temperature(temperature, from_units, to_units):
        """
        Convert temperature between units
        
        Args:
            temperature: Temperature value
            from_units: Source units ('celsius', 'fahrenheit', 'kelvin')
            to_units: Target units
        
        Returns:
            Converted temperature
        """
        # First convert to Celsius
        if from_units == 'celsius':
            celsius = temperature
        elif from_units == 'fahrenheit':
            celsius = (temperature - 32) * 5/9
        elif from_units == 'kelvin':
            celsius = temperature - 273.15
        else:
            raise ValueError(f'Unknown unit: {from_units}')
        
        # Then convert from Celsius to target
        if to_units == 'celsius':
            return round(celsius, 2)
        elif to_units == 'fahrenheit':
            return round(celsius * 9/5 + 32, 2)
        elif to_units == 'kelvin':
            return round(celsius + 273.15, 2)
        else:
            raise ValueError(f'Unknown unit: {to_units}')
