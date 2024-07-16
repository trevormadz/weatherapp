from flask import Flask, jsonify, request,render_template
import requests

app = Flask(__name__)
api_key = 'deaaf96028e66a40ac696e859a350780'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    weather_data = get_weather(city, api_key)
    return render_template('index.html', weather_data=weather_data)


def get_weather(city, api_key):

  url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
  
  response = requests.get(url)
    
  # location = request.args.get('location')
  if response.status_code ==200:
    data = response.json()

    # Prepare the response
    weather_data = {
        'city': data['name'],
        'temperature': data ['main']['temp'],
        'description': data ['weather'][0]['description'],
        'icon':data ['weather'][0]['icon']
    }

    return weather_data
  else:
   return None

if __name__ == '__main__':
    app.run()
