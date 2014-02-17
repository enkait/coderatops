import django.core.handlers.wsgi
from tornado import httpserver, ioloop, web, wsgi, options

options.define('port', type=int, default=8000)

def main():
    django_app = django.core.handlers.wsgi.WSGIHandler()
    wrapped_django_app = wsgi.WSGIContainer(django_app)
    app = web.Application(
        [
            (r'/static/(.*)', web.StaticFileHandler, {'path': '/home/ec2-user/coderatops/backend/static/'}),
            (r'.*', web.FallbackHandler, dict(fallback=wrapped_django_app)),
        ]
    )
    server = httpserver.HTTPServer(app)
    server.listen(options.options.port)
    ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
