from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class WeatherHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/data/2.5/weather"):
            response = {
                "coord": {"lon": -99.13, "lat": 19.43},
                "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}],
                "main": {"temp": 28, "pressure": 1010, "humidity": 40, "temp_min": 27, "temp_max": 29},
                "name": "Ciudad de México",
                "cod": 200
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404, "Not Found")

def run(server_class=HTTPServer, handler_class=WeatherHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Servidor web iniciado en http://localhost:{port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
