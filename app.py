from services import make_service

if __name__ == '__main__':
    make_service('manager').set_port(5000).fire()
