from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/places')
def search_places():
    # Hardcode the search query
    query = 'MVJ College of Engineering'

    # Build the API request URL
    url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key=AIzaSyAfWP_iKshvMZmoUhz4VKXC4y3xoDTmE-4'

    # Send the API request and get the response
    response = requests.get(url)
    data = response.json()

    # Extract the list of places from the response data
    places = data['results']

    # Convert the list of places to a list of dictionaries
    results = [{'name': place['name'], 'address': place['formatted_address']} for place in places]
    print(results)
    # Return the results as a JSON response
    return jsonify(results)
