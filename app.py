from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_client_ip(req):
    forwarded = req.headers.get('X-Forwarded-For')
    return forwarded.split(',')[0] if forwarded else request.remote_addr

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Visitor')
    client_ip = get_client_ip(request)

    try:
        # Use a geolocation service to get the location based on IP
        geo_response = requests.get(f'https://ipapi.co/{client_ip}/json/')
        geo_data = geo_response.json()
        location = geo_data['city']

        # Use a weather service to get the temperature
        weather_response = requests.get('https://api.open-meteo.com/v1/forecast', params={
            'latitude': geo_data['latitude'],
            'longitude': geo_data['longitude'],
            'current_weather': True
        })
        weather_data = weather_response.json()
        temperature = weather_data['current_weather']['temperature']

        return jsonify({
            'client_ip': client_ip,
            'location': location,
            'greeting': f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
