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
        res+= '# HELP rq_total Total HTTP requests\n'
        res+= '# TYPE rq_total counter\n'
        res+= 'rq_total ' + str(sum(self.counters.values())) +'\n'
        res+= '# HELP rq_200_ok 200/OK HTTP requests\n'
        res+= '# TYPE rq_200_ok counter\n'
        res+= 'rq_200_ok '+ str(self.counters[200]) +'\n'
        res+= '# HELP rq_404_nf 404/not found HTTP requests\n'
        res+= '# TYPE rq_404_nf counter\n'
        res+= 'rq_404_nf '+ str(self.counters[404]) +'\n'
        self.textResponse(res)

httpServer = HTTPServer(('', 8080), Servant)
httpServer.serve_forever()