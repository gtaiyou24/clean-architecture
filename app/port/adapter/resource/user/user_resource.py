from fastapi import Depends, APIRouter

from application.identity.dpo import UserDpo
from port.adapter.resource import APIResource
from port.adapter.resource.dependency import get_current_active_user
from port.adapter.resource.user.response import UserJson


class UserResource(APIResource):
    router = APIRouter(prefix='/users', tags=['User'])

    def __init__(self):
        self.router.add_api_route('/me', self.read_users_me, methods=['GET'], response_model=UserJson)

    def read_users_me(self, current_user: UserDpo = Depends(get_current_active_user)) -> UserJson:
        return UserJson.from_(current_user)
