from fastapi import APIRouter

from port.adapter.resource import APIResource


class HealthResource(APIResource):
    router = APIRouter(prefix='/health', tags=['Health'])

    def __init__(self):
        self.router.add_api_route('/check', self.check, methods=['GET'])

    def check(self) -> str:
        return 'OK'
