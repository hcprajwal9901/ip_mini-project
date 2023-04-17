from flask import Flask, render_template , request
import requests,json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("ip1.html")


@app.route('/popular-places', methods=['GET'])
def popular_places():
    # Get the user's location, radius, and datetime
    query = request.args.get('destination')

    #radius = request.args.get('radius')
    #datetime = request.args.get('datetime')

    # Convert the datetime string to a Unix timestamp
    # timestamp = int(datetime.timestamp())

    # Make a request to the Google Places API
    api_key = 'AIzaSyAfWP_iKshvMZmoUhz4VKXC4y3xoDTmE-4'
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&key={}'.format(query, api_key)
    response = requests.get(url)

    results = json.loads(response.text)['results']
    places = []
    for result in results:
        name = result['name']
        address = result['formatted_address']
        rating = result.get('rating', 'N/A')
        photo_reference = result.get('photos', [])[0].get('photo_reference', '') if result.get('photos', []) else ''
        photo_url = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={}&key={}'.format(photo_reference, api_key) if photo_reference else ''
        places.append({'name': name, 'address': address, 'rating': rating, 'photo_url': photo_url})

    # Render the search results template
    return render_template('results.html', query=query, places=places)
if __name__ == '__main__':
    app.run(debug=True)





