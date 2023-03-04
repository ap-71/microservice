from fastapi import HTTPException


class Router:
    def __init__(self, **kwargs):
        self.__services = []
        self.__routes = {
            'get': [],
            'post': [],
            'put': [],
            'delete': []
        }

    @property
    def routes(self):
        return self.__routes

    @property
    def services(self):
        return self.__services

    def add_service(self, service):
        self.__services.append(service)

    def add_route(self, method='get', *args, **kwargs):
        def wrap(func):
            method_ = self.__routes.get(method)
            if method_ is not None:
                method_.append({'args': args, 'func': func})
            else:
                raise HTTPException(status_code=405, detail='Method Not Allowed')
        return wrap

    def add_routes(self, routes):
        for key, key_o in zip(routes, self.__routes):
            self.__routes[key_o] += routes[key]
        print('===')

    def init_routes(self, app):
        method_ = {
            'get': app.get,
            'post': app.post,
            'put': app.put,
            'delete': app.delete
        }
        for key in self.__routes:
            for route in self.__routes[key]:
                m = method_.get(key)
                if m is not None:
                    m(*route['args'])(route['func'])
