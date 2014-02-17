import django.core.handlers.wsgi
from tornado import httpserver, ioloop, web, wsgi, options
from pubsub.pubsub import PubSubWebSocket
from pubsub.pubsub import pub_sub_finder

options.define('http_port', type=int, default=8000)
options.define('ws_port', type=int, default=6379)

def main():
    django_app = django.core.handlers.wsgi.WSGIHandler()
    wrapped_django_app = wsgi.WSGIContainer(django_app)
    http_app = web.Application(
        [
            (r'/static/(.*)', web.StaticFileHandler, {'path': '/home/ec2-user/coderatops/backend/static/'}),
            (r'.*', web.FallbackHandler, dict(fallback=wrapped_django_app)),
        ]
    )
    server = httpserver.HTTPServer(http_app)
    server.listen(options.options.http_port)
    ws_app = web.Application([(r'/ws/(.*)', PubSubWebSocket)])
    ws_app.listen(options.options.ws_port)
    ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
