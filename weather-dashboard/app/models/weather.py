"""Weather data models"""

from datetime import datetime


class Weather:
    """
    Weather data model for current conditions
    """
    def __init__(self, data, units='metric'):
        """
        Initialize Weather object from API response
        
        Args:
            data: API response data
            units: Temperature units
        """
        self.city = data.get('name', '')
        self.country = data.get('sys', {}).get('country', '')
        self.temperature = data.get('main', {}).get('temp', 0)
        self.feels_like = data.get('main', {}).get('feels_like', 0)
        self.temp_min = data.get('main', {}).get('temp_min', 0)
        self.temp_max = data.get('main', {}).get('temp_max', 0)
        self.humidity = data.get('main', {}).get('humidity', 0)
        self.pressure = data.get('main', {}).get('pressure', 0)
        self.wind_speed = data.get('wind', {}).get('speed', 0)
        self.wind_direction = data.get('wind', {}).get('deg', 0)
        self.cloudiness = data.get('clouds', {}).get('all', 0)
        self.weather = data.get('weather', [{}])[0].get('main', '')
        self.weather_description = data.get('weather', [{}])[0].get('description', '')
        self.icon = data.get('weather', [{}])[0].get('icon', '')
        self.sunrise = self._parse_timestamp(data.get('sys', {}).get('sunrise'))
        self.sunset = self._parse_timestamp(data.get('sys', {}).get('sunset'))
        self.timestamp = datetime.now().isoformat()
        self.units = units
    
    def _parse_timestamp(self, timestamp):
        """Parse Unix timestamp to ISO format"""
        if timestamp:
            return datetime.fromtimestamp(timestamp).isoformat() + 'Z'
        return None
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'city': self.city,
            'country': self.country,
            'temperature': self.temperature,
            'feels_like': self.feels_like,
            'temp_min': self.temp_min,
            'temp_max': self.temp_max,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'wind_speed': self.wind_speed,
            'wind_direction': self.wind_direction,
            'cloudiness': self.cloudiness,
            'weather': self.weather,
            'weather_description': self.weather_description,
            'icon': self.icon,
            'sunrise': self.sunrise,
            'sunset': self.sunset,
            'timestamp': self.timestamp,
            'units': self.units
        }


class Forecast:
    """
    Weather forecast data model
    """
    def __init__(self, forecast_list, units='metric'):
        """
        Initialize Forecast object
        
        Args:
            forecast_list: List of forecast items from API
            units: Temperature units
        """
        self.forecasts = []
        for item in forecast_list:
            forecast_item = {
                'date': datetime.fromtimestamp(item.get('dt')).date().isoformat(),
                'temp': item.get('main', {}).get('temp', 0),
                'temp_max': item.get('main', {}).get('temp_max', 0),
                'temp_min': item.get('main', {}).get('temp_min', 0),
                'humidity': item.get('main', {}).get('humidity', 0),
                'pressure': item.get('main', {}).get('pressure', 0),
                'weather': item.get('weather', [{}])[0].get('main', ''),
                'weather_description': item.get('weather', [{}])[0].get('description', ''),
                'icon': item.get('weather', [{}])[0].get('icon', ''),
                'wind_speed': item.get('wind', {}).get('speed', 0),
                'cloudiness': item.get('clouds', {}).get('all', 0),
                'rain': item.get('rain', {}).get('3h', 0),
                'snow': item.get('snow', {}).get('3h', 0)
            }
            self.forecasts.append(forecast_item)
        self.units = units
    
    def to_list(self):
        """Convert to list of dictionaries"""
        return self.forecasts
