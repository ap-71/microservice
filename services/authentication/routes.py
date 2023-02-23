from .typing import User
from ..base_service import Router

router = Router()


@router.add_route('get', '/test')
async def root():
    return {'result': 'ok'}


@router.add_route('post', '/check')
async def root(user: User):
    return user
