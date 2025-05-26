# servidor_flask.py
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/clima", methods=["GET"])
def obtener_clima():
    ciudad_id = request.args.get("id")
    datos = {
        "3995465": {
            "name": "Monterrey",
            "main": {"temp": 25},
            "weather": [{"main": "Haze"}],
            "cod": 200
        },
        "3530597": {
            "name": "CDMX",
            "main": {"temp": 22},
            "weather": [{"main": "Clear"}],
            "cod": 200
        }
    }
    return jsonify(datos.get(ciudad_id, {"cod": 404, "message": "Ciudad no encontrada"}))

if __name__ == "__main__":
    app.run(port=5000)
