# WSWikiGeoOpenSpotify.py

from flask import Flask, request, render_template_string
import wikipedia
import requests
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

app = Flask(__name__)

GEONAMES_USER = 'migfel'
OPENWEATHER_KEY = '152b1599f3e42d9d0f559bf3cf348a2b'
SPOTIFY_CLIENT_ID = 'ce5f91a578f94e2bb2b64674862811a8'
SPOTIFY_CLIENT_SECRET = '45dcefd3a70e461cb11a5ace18ba354a'

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

@app.route('/', methods=['GET', 'POST'])
def index():
    data = {}
    if request.method == 'POST':
        place = request.form['place']
        try:
            description = wikipedia.summary(place, sentences=2)
        except:
            description = 'No se encontró descripción en Wikipedia.'

        geo_url = f'http://api.geonames.org/searchJSON?q={place}&maxRows=1&username={GEONAMES_USER}'
        geo_resp = requests.get(geo_url).json()

        if geo_resp['geonames']:
            geo_info = geo_resp['geonames'][0]
            lat = geo_info.get('lat')
            lng = geo_info.get('lng')
            details = {
                'country': geo_info.get('countryName'),
                'lat': lat,
                'lng': lng,
                'population': geo_info.get('population')
            }

            weather_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={OPENWEATHER_KEY}&units=metric&lang=es'
            weather_resp = requests.get(weather_url).json()
            temperatura = weather_resp['main']['temp']
            descripcion_clima = weather_resp['weather'][0]['description']
            clima = {
                'temperatura': temperatura,
                'descripcion': descripcion_clima
            }

            if temperatura > 20:
                query = "pop español"
            else:
                query = "rock en español"

            results = sp.search(q=query, type='track', limit=1)
            cancion = results['tracks']['items'][0]['name'] + " - " + results['tracks']['items'][0]['artists'][0]['name']

        else:
            details = {'error': 'No se encontró información en GeoNames.'}
            clima = {}
            cancion = "No disponible"

        data = {
            'place': place,
            'description': description,
            'details': details,
            'clima': clima,
            'cancion': cancion
        }

    return render_template_string("""
        <form method="post">
            Lugar: <input name="place">
            <input type="submit">
        </form>
        {% if data %}
            <h2>{{ data.place }}</h2>
            <p><strong>Descripción:</strong> {{ data.description }}</p>
            <p><strong>Detalles:</strong> {{ data.details }}</p>
            <p><strong>Clima:</strong> {{ data.clima }}</p>
            <p><strong>Canción recomendada:</strong> {{ data.cancion }}</p>
        {% endif %}
    """, data=data)

if __name__ == '__main__':
    app.run(debug=True)
