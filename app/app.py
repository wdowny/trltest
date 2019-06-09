from http.server import HTTPServer, BaseHTTPRequestHandler

class Servant(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('Hello, world!'.encode())


httpServer = HTTPServer(('localhost', 8080), Servant)
httpServer.serve_forever()