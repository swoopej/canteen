import re

class RouteException(Exception):
    pass

class Route(object):
    def __init__(self, route, func, request_methods):
        self.callback = func
        # error check on request_methods (lowercase, bad HTTP verbs)
        self.request_methods = request_methods if type(request_methods) is list else [request_methods]
        self.route, self.dynamic = _form_route(route)

    def __eq__(self, r):
        if not isinstance(r, Route):
            return False

        if not (hasattr(r, 'route') and hasattr(r, 'request_methods')):
            return False

        if sorted(self.request_methods) == r.request_methods and \
           self.route == r.route:
           return True

        return False

    def __repr__(self):
        return '<Route: ' + self.route + '>'

    def get_methods(self):
        return self.request_methods

def _form_route(route):
    if not route:
        raise RouteException("'route' cannot be an empty str.")
    if not route.startswith('/'):
        raise RouteException("'route' must begin with a '/'.")

    valid_route = r"/(\w+|<\w+>|<int:\w+>)"
    reg_elts = re.findall(valid_route, route)
    rebuilt_route = '/' + '/'.join(reg_elts)

    if route.endswith('/'):
        rebuilt_route += '/'

    if rebuilt_route != route:
        raise RouteException('Invalid routing path.')

    reg_route = ''
    dynamic = False
    for elt in reg_elts:
        if '<' not in elt:
            reg_route += '/' + elt
            continue

        if re.match('<\w+>', elt):
            dynamic = True
            reg_route += '/(\w+)'
        elif re.match('<int:\w+>', elt):
            dynamic = True
            reg_route += '/(\d+)'
        else:
            assert False, 'Some wack shit happened'

    if route.endswith('/'):
        reg_route += '/'

    # We are looking for *exact* route matches
    reg_route += '$'
    return reg_route, dynamic
