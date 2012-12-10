import thread
import urlparse
import re
import cgitb

from wsgiref.simple_server import make_server
from cgi import escape

from rule import Route

#cgitb.enable()

class Canteen(object):
    def __init__(self):
        self.routes = []

    def run_server(self):
        #instantiate the wsgi server
        #receives request, passes to wsgi app
        #send app's response to client
        httpd = make_server(
            'localhost', 
            8051,
            self.wsgi_app
            )

        httpd.serve_forever()

    def wsgi_app(self, environ, start_response):
        '''
        called by the server with the environ dict and the start_response function
        
        environ must contain CGI/WSGI variables like PATH_INFO, QUERY_STRING, etc. 

        start_response must be called to start the http response.  

        This function will
        return the response body as an iterable.
        '''

        request.update(environ)
        callback, callback_args, method = self.route_request(environ)

        if callback:
            response_body = callback(*callback_args)
            status = "200 OK"
        else:
            response_body = "That is an unknown path"
            status = "404 Not Found"

        response_headers = self.set_headers(response_body)

        start_response(status, response_headers)
        return [response_body]

    def route_request(self, environ):
        path = environ['PATH_INFO']
        request_method = environ['REQUEST_METHOD']

        # The environ variable CONTENT_LENGTH may be empty or missing
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            wsgi_input = environ['wsgi.input'].read(request_body_size)
        except (ValueError):
            request_body_size = 0

        # Search through routes for best match. Dynamic routes should
        # be secondary to absolute routes
        self.routes = sorted(self.routes, key=lambda x: x.dynamic)
        for route in self.routes:
            match = re.match(route.route, path)
            if match and request_method in route.get_methods():
                return route.callback, match.groups(), request_method

        return None, None, None

    def add_route(self, path, methods= 'GET'):
        '''decorates a user supplied function by adding path to self.routes'''
        def decorator(f):
            r = Route(path, f, methods)
            self.routes.append(r)
        return decorator     

    def set_headers(self, response_body):
        headers = [('Content_Type', 'text/html'),
                    ('Content_Length', str(len(response_body)))]
        return headers

class Request(object): 
    def _init__(self):
        self.method = None
        self.cookies = None

    def update(self, environ):
        assert environ, 'Being passed a bogus environ'
        self.args = urlparse.parse_qs(environ['QUERY_STRING'])
        self.method = environ['REQUEST_METHOD']

        if environ['HTTP_COOKIE']:
            self.cookies = environ['HTTP_COOKIE']

class RequestRouter(object):
    """A router class that dynamically dispatches (using the executing
    thread's id) to the intended request object. Needed if the wsgi
    server implementation is threaded.""" 

    def __init__(self):
        self.reqs = {}

    def _get_or_set_req(self):
        req = self.reqs.get(thread.get_ident())
        if not req:
            req = Request()
            self.reqs[thread.get_ident()] = req
        return req        

    def __getattr__(self, attr):
        req = self._get_or_set_req()
        return getattr(req, attr)

    def __setattr__(self, attr, value):
        # Special case used in constructor
        if attr == 'reqs':
            object.__setattr__(self, attr, value)
            return

        req = self._get_or_set_req()
        setattr(req, attr, value)

    def _remove_req(self):
        del self.reqs[thread.get_ident()]

request = RequestRouter()


if __name__ == "__main__":
    app = Canteen()
    app.run_server()


