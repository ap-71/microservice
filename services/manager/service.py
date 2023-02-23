from typing import List

from fastapi import HTTPException

from services.base_service import Service
from utils.typing import ServiceState


class ManagerService(Service):
    def __init__(self, **kwargs):
        self.__services: List[ServiceState] = []
        super().__init__(name='Manager', registration=False, type='Manager', **kwargs)

    def add(self, service_):
        try:
            self.__services.append(service_)
            return True
        except Exception as err:
            raise HTTPException(status_code=502, detail=str(err))

    def get(self, name=None) -> None or ServiceState:
        for service_ in self.__services:
            if service_.service_name == name:
                return service_

    def get_all(self):
        return self.__services
