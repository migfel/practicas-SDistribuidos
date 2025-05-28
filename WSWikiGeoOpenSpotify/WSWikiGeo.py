# WSWikiGeo.py

from flask import Flask, request, render_template_string
import wikipedia
import requests

app = Flask(__name__)

GEONAMES_USER = 'migfel'  # <-- Reemplaza con tu usuario de GeoNames

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
            details = {
                'country': geo_info.get('countryName'),
                'lat': geo_info.get('lat'),
                'lng': geo_info.get('lng'),
                'population': geo_info.get('population')
            }
        else:
            details = {'error': 'No se encontró información en GeoNames.'}

        data = {'place': place, 'description': description, 'details': details}

    return render_template_string("""
        <form method="post">
            Lugar: <input name="place">
            <input type="submit">
        </form>
        {% if data %}
            <h2>{{ data.place }}</h2>
            <p><strong>Descripción:</strong> {{ data.description }}</p>
            <p><strong>Detalles:</strong> {{ data.details }}</p>
        {% endif %}
    """, data=data)

if __name__ == '__main__':
    app.run(debug=True)
