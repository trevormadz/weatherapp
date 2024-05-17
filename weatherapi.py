from flask import Flask, jsonify, request
import requests
app = Flask(__name__)

@app.route('/weather', methods=['GET'])
def get_weather():
    
  location = request.args.get('location')
  if location:

    # Make a request to a weather API (in this case, OpenWeatherMap API)
    api_key = 'deaaf96028e66a40ac696e859a350780'  # Replace with your actual API key
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}'

    response = requests.get(url)
    data = response.json()

    # Extract the relevant weather information
    temperature = data.get('main', {}).get('temp')
    description = data['weather'][0]['description']

    # Prepare the response
    weather_data = {
        'location': location,
        'temperature': temperature,
        'description': description
    }

    return jsonify(weather_data)
  else:
   return jsonify({"error": "Invalid location provided"}), 400

if __name__ == '__main__':
    app.run()
