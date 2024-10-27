import json, os
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Type
import uuid


# Serwer obsługujący żądania HTTP
class SimpleRequestHandler(BaseHTTPRequestHandler):
    user_list = [{
        'id': str(uuid.uuid4()),
        'first_name': 'Michal',
        'last_name': 'Mucha',
        'role': 'Instructor'
    }]

    # Obsługa zapytań OPTIONS (CORS)
    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self._set_headers()
        self.end_headers()

    # Ustawienia nagłówków HTTP
    def _set_headers(self):
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    # Obsługa zapytań GET (pobieranie danych z serwera)
    def do_GET(self) -> None:
        if self.path == "/":
            self.get_html()
        elif self.path == "/data":
            self.get_data()
        elif self.path == "/styles.css":
            self.get_css()
        elif self.path == "/logic.js":
            self.get_js()

    def get_html(self) -> None:
        self.send_response(200)
        self._set_headers()
        self.end_headers()
        self.wfile.write(json.dumps(SimpleRequestHandler.user_list).encode('utf-8'))

    def get_css(self) -> None:
        filepath = os.path.join(os.path.dirname(__file__), '../nginx/ui_app/styles.css')

        try:
            with open(filepath, 'rb') as index_file:
                css_content = index_file.read()

            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            self.wfile.write(css_content)
        except:
            self.send_error(404, "File not found")

    def get_js(self) -> None:
        filepath = os.path.join(os.path.dirname(__file__), '../nginx/ui_app/logic.js')

        try:
            with open(filepath, 'rb') as index_file:
                js_content = index_file.read()

            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            self.wfile.write(js_content)
        except:
            self.send_error(404, "File not found")

    def get_data(self) -> None:
        # Odpowiedź z danymi (JSON)
        self.send_response(200)
        self._set_headers()
        self.end_headers()

        self.wfile.write(json.dumps(SimpleRequestHandler.user_list).encode('utf-8'))

    # Obsługa POST (przesyłanie danych do serwera)
    def do_POST(self) -> None:
        if self.path == "/team":
            content_type = self.headers.get('Content-Type')
            if content_type == 'application/json':
                content_length = int(self.headers['Content-Length'])  # Pobierz długość treści
                post_data = self.rfile.read(content_length)  # Odczytaj dane POST

                try:
                    # Dekodowanie danych JSON
                    received_data = json.loads(post_data.decode('utf-8'))

                    privacy_policy_accepted = received_data.get("privacy_policy") == "on"
                    correct_role = received_data.get('role') in ["Manager", "Development Lead", "Product Designer", "CTO"]

                    if privacy_policy_accepted and correct_role:
                        SimpleRequestHandler.user_list.append({
                            'id': str(uuid.uuid4()),
                            'first_name': received_data.get("first_name"),
                            'last_name': received_data.get("last_name"),
                            'role': received_data.get("role"),
                        })

                    self.send_response(201)
                    self._set_headers()
                    self.end_headers()

                except json.JSONDecodeError:
                    # Obsługa błędów dekodowania JSON
                    self.send_response(400)
                    self._set_headers()
                    self.end_headers()
                    self.wfile.write(b'Invalid JSON')
            else:
                # Jeśli content type nie jest JSON, zwróć błąd
                self.send_response(415)
                self._set_headers()
                self.end_headers()
                self.wfile.write(b'Unsupported Media Type')

    # Obsługa zapytań DELETE (usuwanie użytkowników)
    def do_DELETE(self):
        if self.path.startswith("/delete/"):
            try:
                user_id = self.path.split('/')[-1]  # Pobierz id z URL

                initial_count = len(SimpleRequestHandler.user_list)
                SimpleRequestHandler.user_list = [user for user in SimpleRequestHandler.user_list if user['id'] != user_id]

                if len(SimpleRequestHandler.user_list) < initial_count:
                    self.send_response(200)
                else:
                    self.send_response(404)


                self._set_headers()
                self.end_headers()

            except ValueError:
                self.send_response(400)  # Błędny format indeksu
                self._set_headers()
                self.end_headers()

# Uruchomienie serwera HTTP
def run(
        server_class: Type[HTTPServer] = HTTPServer,
        handler_class: Type[BaseHTTPRequestHandler] = SimpleRequestHandler,
        port: int = 8080
) -> None:
    # zdefiniowanie adresu serwera
    server_address: tuple = ('', port)

    # Utworzenie serwera HTTP
    httpd: HTTPServer = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {port}...")

    # Uruchomienie serwera
    httpd.serve_forever()


if __name__ == '__main__':
    run()

