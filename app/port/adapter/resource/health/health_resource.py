from fastapi import APIRouter


class HealthResource:
    router = APIRouter(prefix='/health', tags=['Health'])

    def __init__(self):
        self.router.add_api_route('/check', self.check, methods=['GET'])

    def check(self) -> dict:
        return {'health': True}
