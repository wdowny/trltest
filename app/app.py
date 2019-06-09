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
        self.wfile.write('Sorry, nothing was found by your request.'.encode())
        self.counters[404]+=1

    def do_GET(self):
        try:
            getattr(self, 'evt_'+self.router[self.path])()
        except:
            self.defaultResponse()
        
    def evt_index(self):
        self.httpResponse('Hello, TR Logic!<br>Pirates of the Caribbean welcome you!')
        
    def evt_metrics(self):
        res = 'rq_total ' + str(sum(self.counters.values())) +'\n'
        res+= 'rq_200_ok '+ str(self.counters[200]) +'\n'
        res+= 'rq_404_nf '+ str(self.counters[404]) +'\n'
        self.textResponse(res)

httpServer = HTTPServer(('', 8080), Servant)
httpServer.serve_forever()