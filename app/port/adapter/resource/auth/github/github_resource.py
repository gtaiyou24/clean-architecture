import requests
from di import DIContainer
from fastapi import APIRouter, Depends

from application.identity import IdentityApplicationService
from application.identity.command import AuthenticateUserCommand
from port.adapter.resource.auth.github.request import AccessTokenRequest
from port.adapter.resource.auth.response import Token


class GitHubResource:
    router = APIRouter(prefix='/auth/github', tags=['Auth'])
    GITHUB_API = 'https://api.github.com'

    def __init__(self, client_id: str, client_secret: str):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.router.add_api_route("/token", self.token, methods=["POST"], response_model=Token)

    def token(self, request: AccessTokenRequest = Depends()) -> Token:
        # 一時コード指定で GitHub からアクセストークンを取得する
        access_token = requests.post(
            'https://github.com/login/oauth/access_token',
            headers={'Accept': 'application/json'},
            params={'client_id': self.__client_id, 'client_secret': self.__client_secret, 'code': request.code}
        ).json()

        # アクセストークン指定で GitHub からユーザー情報、メールアドレスを取得する
        headers = {'Authorization': f"Bearer {access_token['access_token']}"}
        user = requests.get(f'{self.GITHUB_API}/user', headers=headers).json()
        emails = requests.get(f'{self.GITHUB_API}/user/emails', headers=headers).json()

        # 認証
        command = AuthenticateUserCommand.github(user, emails)
        application_service = DIContainer.instance().resolve(IdentityApplicationService)
        dpo = application_service.authenticate_github_user(command)

        # アクセストークンを発行
        return Token.generate(dpo)
