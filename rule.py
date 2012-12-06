import re

class Route(object):
    def __init__(self, route, func, request_methods):
        self.callback = func
        self.request_methods = request_methods
        self.route, self.dynamic = _form_route(route)

    def get_methods(self):
        return self.request_methods

def _form_route(route):
    valid_route = r"/(\w+|<str:\w+>|<int:\w+>)"
    reg_elts = re.findall(valid_route, route)
    rebuilt_route = '/' + '/'.join(reg_elts)
    if rebuilt_route != route and rebuilt_route + '/' != route:
        raise Exception('Invalid routing path.')

    route = ''
    dynamic = False
    for elt in reg_elts:
        if '<' not in elt:
            route += '/' + elt
            continue

        if re.match('<str:\w+>', elt):
            dynamic = True
            route += '/(\w+)'
        elif re.match('<int:\w+>', elt):
            dynamic = True
            route += '/(\d+)'
        else:
            assert False, 'Some wack shit happened'

    return route, dynamic
