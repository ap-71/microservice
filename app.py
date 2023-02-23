from services import make_service

if __name__ == '__main__':
    manager = make_service('manager')
    manager.set_port(5000).fire()

