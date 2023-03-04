import requests
from fastapi import HTTPException, FastAPI

from utils.typing import State, ServiceState
from utils.wrap_exception import wrap_except
from .router import Router


class Service:
    def __init__(self, **kwargs):
        self.__host = kwargs.get('host', '127.0.0.1')
        self.__app = kwargs.get('app', FastAPI())
        self.__type = kwargs.pop('type')
        self.__name = kwargs.pop('name') + 'Service'
        self.__session = requests.Session()
        self.__log_level = kwargs.get('log_level', 'info')
        self.__reload = kwargs.get('reload', False)
        self.__port = kwargs.get('port', 49100)
        self.__url_manager = kwargs.get('url_manager', 'http://localhost:5000/{action}')
        self.__registration_to_manager = kwargs.get('registration', True)
        self.__state = State.stop
        self.__router: Router = kwargs.get('router')
        if self.__router is not None:
            self.__router.add_service(self)

    @property
    def app(self):
        return self.__app

    @property
    def router(self):
        return self.__router

    @router.setter
    def router(self, val):
        self.__router = val

    @wrap_except
    def registration(self, url=None):
        if not self.__registration_to_manager:
            return {'data': 'registration to manager is NONE'}
        self.__state = State.running.value
        url = url if url is not None else self.__url_manager
        url = url.replace('{action}', 'registration')
        resp = self.__session.post(url,
                                   data=self.make_service_state(),
                                   headers={'Content-type': 'application/json'})
        return resp

    def add_route(self, method='get', *args, **kwargs):
        method_ = {
            'get': self.__app.get,
            'post': self.__app.post,
            'put': self.__app.put,
            'delete': self.__app.delete
        }.get(method)

        return method_(*args) if method_ is not None else HTTPException(status_code=405, detail='Method Not Allowed')

    def make_service_state(self, **kwargs):
        _service_name = kwargs.get('service_name', self.__name)
        _state = kwargs.get('state', self.__state)
        _type = kwargs.get('type', self.__type)
        _host = kwargs.get('host', self.__host)
        _port = kwargs.get('port', self.__port)
        return ServiceState(
            service_name=_service_name,
            state=_state,
            type=_type,
            host=_host,
            port=_port
        ).json()

    def set_state(self, state: State):
        if state != self.__state:
            url = self.__url_manager.replace('{action}', 'state/' + self.__name)
            session = self.__session
            data = self.make_service_state(state=state.value)
            headers = {'Content-type': 'application/json'}
            session.put(url, data=data, headers=headers)
            self.__state = state

    def set_port(self, port: int):
        self.__port = port
        return self

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port: int):
        self.__port = port

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, val):
        self.__name = val

    def fire(self):
        import uvicorn
        self.router.init_routes(self.__app)
        self.registration()
        try:
            uvicorn.run(self.__app, host=self.__host, port=self.__port, log_level=self.__log_level,
                        reload=self.__reload)
        except Exception as e:
            print(str(e))
        self.set_state(State.stop)
