import http.server
import socketserver
import json

PORT = 8000

class LoginHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        # We only handle the /api/login endpoint
        if self.path == '/api/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse the JSON payload from frontend
                data = json.loads(post_data.decode('utf-8'))
                email = data.get('email')
                password = data.get('password')
                
                # Basic mock validation: in a real app, check against a database!
                if email and len(password) >= 3:
                    # Success case
                    response = {'status': 'success', 'message': 'Login successful!'}
                    self.send_response(200)
                else:
                    # Failure case
                    response = {'status': 'error', 'message': 'Invalid credentials'}
                    self.send_response(401)
                    
            except json.JSONDecodeError:
                response = {'status': 'error', 'message': 'Invalid JSON format'}
                self.send_response(400)
                
            # Send the response headers and JSON data back
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            # If they post anywhere else, return 404
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

# Allow reusing the port so we don't get 'Address already in use' errors
socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), LoginHandler) as httpd:
    print(f"Server starting on port {PORT}...")
    print(f"You can view the app at http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
