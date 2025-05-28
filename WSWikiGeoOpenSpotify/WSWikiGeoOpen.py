# WSWikiGeoOpen.py

from flask import Flask, request, render_template_string
import wikipedia
import requests
import os

app = Flask(__name__)

GEONAMES_USER = 'tu usuario '
OPENWEATHER_KEY = 'tu api key de openweather'

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
            clima = {
                'temperatura': weather_resp['main']['temp'],
                'descripcion': weather_resp['weather'][0]['description']
            }

        else:
            details = {'error': 'No se encontró información en GeoNames.'}
            clima = {}

        data = {'place': place, 'description': description, 'details': details, 'clima': clima}

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
        {% endif %}
    """, data=data)

if __name__ == '__main__':
    app.run(debug=True)
