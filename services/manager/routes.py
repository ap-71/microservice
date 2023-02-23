from fastapi import HTTPException

from utils.typing import ServiceState
from ..base_service.router import Router

router = Router()


@router.add_route('get', "/state")
async def read_services_state():
    service = router.services[0]
    return service.get_all()


@router.add_route('get', "/state/{service_name}")
async def read_service_state(service_name: str):
    service = router.services[0]
    service_ = service.get(service_name)
    if service_ is not None:
        return service_
    raise HTTPException(status_code=404, detail="Service not found")


@router.add_route('put', "/state/{service_name}")
async def update_service_state(service_name: str, current_service: ServiceState):
    service = router.services[0]
    service_ = service.get(current_service.service_name)
    if service_ is not None:
        service_.state = current_service.state
        return service_
    raise HTTPException(status_code=404, detail="Service not found")


@router.add_route('post', "/registration")
async def registration_service(current_service: ServiceState):
    service = router.services[0]
    if service.get(current_service.service_name) is None:
        result = service.add(current_service)
        return {'service': current_service, 'result': result}
    return HTTPException(status_code=400, detail=f'Service is exists with name {current_service.service_name}')
