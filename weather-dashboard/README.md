# Weather Dashboard Application

A full-featured weather application that fetches real-time weather data from OpenWeatherMap API with a beautiful web interface.

## 🌟 Features

- ✅ Real-time weather data from OpenWeatherMap API
- ✅ Current weather conditions (temperature, humidity, wind speed, pressure)
- ✅ 5-day weather forecast
- ✅ Multiple city search
- ✅ Temperature unit conversion (Celsius/Fahrenheit)
- ✅ Weather icons and descriptions
- ✅ Responsive design (Desktop, Tablet, Mobile)
- ✅ Recent searches history
- ✅ API response caching
- ✅ Error handling and validation
- ✅ Beautiful UI with modern design
- ✅ Unit tests for backend

## 📋 Project Structure

```
weather-dashboard/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── weather.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── weather_routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── weather_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   ├── cache.py
│   │   └── exceptions.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   └── 404.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── script.js
├── config.py
├── run.py
├── requirements.txt
├── .env.example
├── test_weather.py
└── README.md
```

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip
- OpenWeatherMap API key (free at https://openweathermap.org/api)

### Step 1: Clone Repository
```bash
git clone https://github.com/ankithkumarreddyk24cs-bit/Python-Functions.git
cd weather-dashboard
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables
```bash
cp .env.example .env
```

Edit `.env` and add your OpenWeatherMap API key:
```env
OPENWEATHERMAP_API_KEY=your_api_key_here
FLASK_ENV=development
FLASK_PORT=5000
CACHE_TIMEOUT=600
```

### Step 5: Run Application
```bash
python run.py
```

**Visit: http://localhost:5000**

## 📚 API Endpoints

### Get Current Weather
**Endpoint:** `GET /api/weather/current`

**Query Parameters:**
- `city` (string, required): City name
- `units` (string, optional): 'metric' or 'imperial' (default: 'metric')

**Example:**
```bash
curl "http://localhost:5000/api/weather/current?city=London"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "city": "London",
    "country": "GB",
    "temperature": 15.5,
    "feels_like": 14.8,
    "humidity": 72,
    "pressure": 1013,
    "wind_speed": 4.5,
    "weather": "Partly cloudy",
    "icon": "02d",
    "sunrise": "2024-01-15T07:45:00Z",
    "sunset": "2024-01-15T16:30:00Z"
  }
}
```

### Get Weather Forecast
**Endpoint:** `GET /api/weather/forecast`

**Query Parameters:**
- `city` (string, required): City name
- `units` (string, optional): 'metric' or 'imperial'
- `days` (integer, optional): Number of days (default: 5, max: 5)

**Example:**
```bash
curl "http://localhost:5000/api/weather/forecast?city=London&days=5"
```

### Search Cities
**Endpoint:** `GET /api/weather/search`

**Query Parameters:**
- `query` (string, required): Partial city name

**Example:**
```bash
curl "http://localhost:5000/api/weather/search?query=London"
```

### Convert Temperature
**Endpoint:** `POST /api/weather/convert`

**Request Body:**
```json
{
  "temperature": 20,
  "from_units": "celsius",
  "to_units": "fahrenheit"
}
```

**Example:**
```bash
curl -X POST "http://localhost:5000/api/weather/convert" \
  -H "Content-Type: application/json" \
  -d '{"temperature": 20, "from_units": "celsius", "to_units": "fahrenheit"}'
```

## 🎨 Web Interface

### Current Weather Display
- Large temperature display
- Weather condition with icon
- Feels like temperature
- Humidity level
- Wind speed
- Pressure
- Sunrise/Sunset times

### 5-Day Forecast
- Daily temperature (min/max)
- Weather conditions
- Humidity
- Wind speed

### Search Features
- Real-time city search
- Search history
- Suggestions dropdown
- Temperature unit toggle

## 🧪 Testing

Run tests:
```bash
python -m unittest test_weather.py -v
```

Test coverage includes:
- API endpoint tests
- Weather service tests
- Validation tests
- Cache tests
- Error handling tests
- Temperature conversion tests

## 🔑 API Key Setup

1. Visit https://openweathermap.org/api
2. Create a free account
3. Generate an API key
4. Add to `.env` file:
   ```
   OPENWEATHERMAP_API_KEY=your_key_here
   ```

## 📦 Technologies Used

| Technology | Version | Purpose |
|-----------|---------|----------|
| Flask | 2.3.3 | Web framework |
| Requests | 2.31.0 | HTTP requests |
| Python-dotenv | 1.0.0 | Environment variables |
| Flask-Caching | 2.0.2 | Response caching |
| Bootstrap | 5.3 | UI Framework |
| JavaScript | ES6+ | Frontend interactivity |

## 🌐 Weather Icons

Weather conditions are represented with beautiful SVG icons:
- ☀️ Sunny
- 🌤️ Partly Cloudy
- ☁️ Cloudy
- 🌧️ Rainy
- ⛈️ Thunderstorm
- ❄️ Snow
- 🌫️ Fog

## 💾 Caching

API responses are cached for 10 minutes (configurable) to:
- Reduce API calls
- Improve response time
- Stay within API rate limits

## ⚙️ Configuration

### Environment Variables
```env
# OpenWeatherMap API
OPENWEATHERMAP_API_KEY=your_api_key

# Flask Settings
FLASK_ENV=development
FLASK_PORT=5000
SECRET_KEY=your_secret_key

# Caching
CACHE_TIMEOUT=600
CACHE_TYPE=simple

# Logging
LOG_LEVEL=INFO
```

## 📱 Responsive Design

Optimized for:
- 📱 Mobile devices (320px+)
- 📱 Tablets (768px+)
- 💻 Desktops (1024px+)
- 🖥️ Large screens (1440px+)

## ⚠️ Error Handling

Comprehensive error handling for:
- Invalid city names
- API rate limits
- Network errors
- Invalid API keys
- Server errors

## 🚀 Deployment

### Heroku Deployment
```bash
heroku create weather-dashboard-app
git push heroku main
heroku config:set OPENWEATHERMAP_API_KEY=your_key
heroku open
```

### Docker Deployment
```bash
docker build -t weather-dashboard .
docker run -p 5000:5000 -e OPENWEATHERMAP_API_KEY=your_key weather-dashboard
```

## 🐛 Troubleshooting

### Issue: "API key not found"
**Solution:** Check `.env` file and ensure `OPENWEATHERMAP_API_KEY` is set

### Issue: "City not found"
**Solution:** Try searching with a simpler city name or country code

### Issue: "Rate limit exceeded"
**Solution:** Wait a few minutes or upgrade your API plan

### Issue: "Site can't be reached"
**Solution:** 
1. Make sure Flask is running: `python run.py`
2. Check that port 5000 is not in use
3. Visit http://localhost:5000 (not https)

## 📞 Support

For issues or questions:
1. Check the documentation
2. Review test cases
3. Check API status at openweathermap.org

## 📄 License

MIT License - Feel free to use and modify

## 🙏 Acknowledgments

- OpenWeatherMap for weather data
- Flask community
- Bootstrap for UI

---

**Last Updated:** January 2024
**Author:** ankithkumarreddyk24cs-bit
**Version:** 1.0.0
**Repository:** [Python-Functions](https://github.com/ankithkumarreddyk24cs-bit/Python-Functions)
