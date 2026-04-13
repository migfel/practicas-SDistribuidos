from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "TU_API_KEY"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route("/clima", methods=["GET"])
def clima():
    ciudad = request.args.get("ciudad", "")

    if not ciudad:
        return jsonify({"error": "Falta el parámetro 'ciudad'"}), 400

    params = {
        "q": ciudad,
        "units": "metric",
        "appid": API_KEY,
        "lang": "es"
    }

    try:
        respuesta = requests.get(BASE_URL, params=params, timeout=10)
        data = respuesta.json()

        if data.get("cod") != 200:
            return jsonify({"error": data.get("message")})

        return jsonify({
            "ciudad": data["name"],
            "temperatura": data["main"]["temp"],
            "humedad": data["main"]["humidity"],
            "clima": data["weather"][0]["description"]
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)