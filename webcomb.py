

"""
    http://blog.zoom.nu/2010/05/parser-combinators-in-python.html
"""



class WebCombinator:
    def __init__(self, f, g=None):
        self.f = f
        if g:
            self.g = g
        else:
            self.g = None

    def __call__(self, environ, start_response):
        '''
            must be wsgi compatible
        '''
        x = self.f(environ, start_response)

        #FIXME
        if self.g:
            y = self.g(environ, start_response)

        return x

    def __pow__(self, right):
        '''
            composite of f and g.
            we use **, due to righthand
            (h ** g ** f )(x) == h(g(f(x)))
        '''
        return WebCombinator(self, right)


if __name__ == '__main__':
    from wsgiref.validate import validator
    from wsgiref.simple_server import make_server

    def hello(environ, start_response):
        status = '200 OK'
        headers = [("Content-type", 'text/plain')]
        start_response(status, headers)
        return ["hello world!"]

    def bye(environ, start_response):
        #status = '200 OK'
        #headers = [("Content-type", 'text/plain')]
        #start_response(status, headers)
        return ["bye!"]


    w = WebCombinator(bye) ** WebCombinator(hello) 
    validator_app = validator(w)

    httpd = make_server('', 8000, validator_app)
    print "Listening on port 8000"
    httpd.serve_forever()

