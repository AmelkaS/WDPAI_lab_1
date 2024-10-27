import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Type


class SimpleRequestHandler(BaseHTTPRequestHandler):


    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.send_header("Access-Control-Allow-Origin", "*")

        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")

        self.send_header("Access-Control-Allow-Headers", "Content-Type")

        self.end_headers()

    def do_GET(self) -> None:
        self.send_response(200)

        self.send_header('Content-type', 'application/json')

        self.send_header('Access-Control-Allow-Origin', '*')

        self.end_headers()

        response: dict = {
            "message": "This is a GET request",
            "path": self.path
        }

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self) -> None:

        content_length: int = int(self.headers['Content-Length'])

        post_data: bytes = self.rfile.read(content_length)

        received_data: dict = json.loads(post_data.decode())

        response: dict = {
            "message": "This is a POST request",
            "received": received_data
        }

        # Send the response headers.
        # Set the status to 200 OK and indicate the response content will be in JSON format.
        self.send_response(200)
        self.send_header('Content-type', 'application/json')

        # Again, allow any origin to access this resource (CORS header).
        self.send_header('Access-Control-Allow-Origin', '*')

        # Finish sending headers.
        self.end_headers()

        # Convert the response dictionary to a JSON string and send it back to the client.
        self.wfile.write(json.dumps(response).encode())


# Function to start the server.
# It takes parameters to specify the server class, handler class, and port number.
def run(
        server_class: Type[HTTPServer] = HTTPServer,
        handler_class: Type[BaseHTTPRequestHandler] = SimpleRequestHandler,
        port: int = 8080
) -> None:
    # Define the server address.
    # '' means it will bind to all available network interfaces on the machine, and the port is specified.
    server_address: tuple = ('', port)
    # Create an instance of HTTPServer with the specified server address and request handler.
    httpd: HTTPServer = server_class(server_address, handler_class)
    # Print a message to the console indicating that the server is starting and which port it will listen on.
    print(f"Starting HTTP server on port {port}...")
    # Start the server and make it continuously listen for requests.
    # This method will block the program and keep running until interrupted.
    httpd.serve_forever()


# If this script is executed directly (not imported as a module), this block runs.
# It calls the `run()` function to start the server.
if __name__ == '__main__':
    run()