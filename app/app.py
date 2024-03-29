from http.server import HTTPServer, BaseHTTPRequestHandler
from werkzeug._compat import try_coerce_native

class Servant(BaseHTTPRequestHandler):
    
    counters = {
        200: 0,
        404: 0
        }
    
    router = {
        '/':        'index',
        '/metrics': 'metrics',
        }
    
    def httpResponse(self, content):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content.encode())
        self.counters[200]+=1

    def textResponse(self, content):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(content.encode())
        self.counters[200]+=1


    def defaultResponse(self):        
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('Sorry, nothing was found by your request. <a href="/">Come back.</a>'.encode())
        self.counters[404]+=1

    def do_GET(self):
        try:
            getattr(self, 'evt_'+self.router[self.path])()
        except:
            self.defaultResponse()
        
    def evt_index(self):
        self.httpResponse('''
Hello, TR Logic!
<br>
Pirates of the Caribbean welcome you!
<br><br>
Here is <a href="/metrics">link to metrics</a>. And <a href="/nowhere">this link</a> is broken. 
''')
        
    def evt_metrics(self):
        res = ''
        res+= '# HELP http_requests HTTP requests counter\n'
        res+= '# TYPE http_requests counter\n'
        res+= 'http_requests{code="200"} '+ str(self.counters[200]) +'\n'
        res+= 'http_requests{code="404"} '+ str(self.counters[404]) +'\n'
        self.textResponse(res)

httpServer = HTTPServer(('', 8080), Servant)
httpServer.serve_forever()