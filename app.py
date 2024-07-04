from flask import Flask, request, jsonify
import geoip2.database

app = Flask(__name__)

# Replace 'path/to/GeoLite2-City.mmdb' with the actual path to your GeoIP2 database file
reader = geoip2.database.Reader('path/to/GeoLite2-City.mmdb')

@app.route('/api/hello', methods=['GET'])
def hello_world():
  # Extract visitor name from query parameter
  visitor_name = request.args.get('visitor_name')
  
  # Get visitor's IP address
  client_ip = request.remote_addr
  
  # Use GeoIP2 to get location data based on IP (requires GeoIP2 database)
  try:
      response = reader.city(client_ip)
      location = response.city.names['en']
  except:
      location = "Unknown"

  # Replace with actual temperature retrieval logic (e.g., API call)
  temperature = 11  # Placeholder temperature

  greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celcius in {location}"
  response = {'client_ip': client_ip, 'location': location, 'greeting': greeting}
  return jsonify(response)

if __name__ == '__main__':
  app.run(debug=True)
