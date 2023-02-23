from services.base_service import Service


class AuthService(Service):
    def __init__(self, **kwargs):
        super().__init__(name='Authentication', type='Authentication', **kwargs)
