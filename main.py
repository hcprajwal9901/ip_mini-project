from flask import Flask, render_template, request,session
import requests,sys

app = Flask(__name__)
rating=[]
latitude=0
longitude=0

app.secret_key = 'gofuckyourself'
@app.get('/')
def home():

    return render_template('index.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    global rating
    global longitude
    global  latitude
    radius = request.form.get('radius')
    
    place_types = request.form.getlist('placeType')
    latitude=request.form.get('latitude')
    longitude=request.form.get('longitude')
    # Do something with the retrieved values, such as storing them in a database
    
    api_key = 'AIzaSyAfWP_iKshvMZmoUhz4VKXC4y3xoDTmE-4'
    if 'all' in place_types:
        url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&key={api_key}'
    else:
        #place_type_str = ','.join(place_types)
         
         url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&keyword={place_types}&key={api_key}'

    #url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&keyword={place_type}&key={api_key}'
    
    response = requests.get(url)
    data = response.json()
    places = data['results']
   

    if not places:
        return render_template('none.html')
      # Initialize the top-rated places list
    max_rating = 0 
    top_rated_places = session.get('top_rated_places', [])
    for place in places:
        place['photo_url'] = place['photos'][0]['photo_reference'] if 'photos' in place else None
        place['rating'] = place.get('rating', None)
        
        if place['rating'] is not None and place['rating'] > max_rating:
            top_rated_places = [place]  # If a higher-rated place is found, replace the top-rated places list
            max_rating = place['rating']
        elif place['rating'] is not None and place['rating'] == max_rating:
            top_rated_places.append(place)  # If a place has the same rating as the current maximum, add it to top-rated places

    rating+=top_rated_places
    for place in rating:
        encoded_name = place['name'].encode(sys.stdout.encoding, errors='replace')
        print(encoded_name.decode())
    
  
    return render_template('places.html', places=places)
    
@app.route('/plan')
def plan():
    
    return render_template('itinerary.html', top_rated_places=rating,user_latitude=latitude,user_longitude=longitude)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

