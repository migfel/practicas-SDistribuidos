from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculadora/sumar')
def sumar():
    a = int(request.args.get('a'))

#http://127.0.0.1:5000/calculadora/sumar/?a=5&b=6

    b = int(request.args.get('b'))
    return jsonify({'resultado': a + b})

@app.route('/calculadora/restar')
def restar():
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    return jsonify({'resultado': a - b})

@app.route('/calculadora/multiplicar')
def multiplicar():
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    return jsonify({'resultado': a * b})

@app.route('/calculadora/dividir')
def dividir():
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    return jsonify({'resultado': a / b})

if __name__ == '__main__':
    app.run(debug=True)
