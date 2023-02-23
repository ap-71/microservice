import importlib


def make_service(name):
    module = importlib.import_module('services.'+name)
    return module.Service(router=module.router)
