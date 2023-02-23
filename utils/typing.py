from enum import IntEnum

from pydantic import BaseModel


class State(IntEnum):
    running = 1
    stop = 0


class ServiceState(BaseModel):
    service_name: str
    state: int
    type: str
    host: str
    port: int
