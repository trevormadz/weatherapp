from flask import Flask, jsonify, request,render_template
import requests

from datetime import datetime


app = Flask(__name__)
api_key = 'deaaf96028e66a40ac696e859a350780'

@app.route('/', methods=['GET', 'POST'])
def index():
    now = datetime.now()
    hour = now.hour
    current_year = now.year

    if 6 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    if request.method == 'POST':
        city = request.form.get('city')
        units = request.form.get('units', 'metric')
        if not city:
            return render_template('index.html', error="Invaild city. Please enter a vaild city name")
        
        weather_data = get_weather_data(city, units)
        if 'error' in weather_data:
            return render_template('index.html', error=weather_data['error'])
        
        forecast_data = get_forecast_data(city, units)
        return render_template('index.html', weather_data=weather_data, forecast_data=forecast_data, units=units)
    return render_template('index.html',greeting=greeting,current_year=current_year)

def get_weather_data(city, units):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}'
    response = requests.get(url).json()
    if response.get('cod') != 200:
        return {'error': response.get('message', 'Error retrieving weather data')}
    
    return {
        'city': response['name'],
        'temperature': response['main']['temp'],
        'feels_like': response['main']['feels_like'],
        'humidity': response['main']['humidity'],
        'wind_speed': response['wind']['speed'],
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon']
    }

def get_forecast_data(city, units):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units={units}'
    response = requests.get(url).json()
    if response.get('cod') != '200':
        return []
    
    forecast_data = []
    for item in response['list']:
        date = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
        formatted_date = date.strftime('%a %d')
        forecast_data.append({
            'date': formatted_date,
            'high_temperature': item['main']['temp_max'],
            'low_temperature': item['main']['temp_min'],
            'icon': item['weather'][0]['icon']
        })
    return forecast_data

if __name__ == '__main__':
    app.run()
