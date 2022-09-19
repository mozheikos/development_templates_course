import sys
from wsgiref.simple_server import make_server

from middleware import middlewares
from urls import urls
from views import router
from web_framework.application import App

application = App()

application.path_register(urls)
application.path_register(router.urls)
application.middleware_register(middlewares)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        host, port = sys.argv[1:]
    else:
        host = ''
        port = 8080

    with make_server(host, int(port), application) as server:
        server.serve_forever()
