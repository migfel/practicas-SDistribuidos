from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/hola", methods=["GET"])
def hola_mundo():
    nombre = request.args.get("nombre", "Mundo")
    return jsonify({"mensaje": f"Hola {nombre}"})

@app.route("/clima", methods=["GET"])
def clima():
    return jsonify({
        "ciudad": "CDMX",
        "clima": {
            "temp": 22,
            "estado": "Soleado",
            "humedad": 45
        }
    })

@app.route("/saludo", methods=["GET"])
def saludo():
    return jsonify({"saludo": "¡Buenos días desde el servidor Flask!"})

@app.route("/hola", methods=["POST"])
def hola_post():
    datos = request.get_json()
    nombre = datos.get("nombre", "Mundo")
    return jsonify({"mensaje": f"Hola {nombre} (vía POST)"})

if __name__ == "__main__":
    app.run(port=5000)
