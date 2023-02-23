import threading
import time

from services import make_service

if __name__ == '__main__':
    thrds = []
    for i in range(3):
        auth_service = make_service('authentication')
        auth_service.name += f'_{i}'
        auth_service.port += i
        thr = threading.Thread(target=auth_service.fire, name=auth_service.name)
        thr.start()
        thrds.append(thr)
    while len([service for service in thrds if service.is_alive()]) > 0:
        time.sleep(3)
