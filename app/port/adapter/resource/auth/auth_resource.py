from __future__ import annotations

from di import DIContainer
from fastapi import APIRouter, Depends

from application.identity import IdentityApplicationService
from application.identity.command import RegisterUserCommand, AuthenticateUserCommand, ForgotPasswordCommand, \
    ResetPasswordCommand
from application.identity.dpo import UserDpo
from port.adapter.resource import APIResource
from port.adapter.resource.auth.request import RegisterUserRequest, OAuth2PasswordRequest, ForgotPasswordRequest, \
    ResetPasswordRequest
from port.adapter.resource.auth.response import UserDescriptorJson, Token
from port.adapter.resource.dependency import get_current_active_user


class AuthResource(APIResource):
    router = APIRouter(prefix='/auth', tags=['Auth'])

    def __init__(self):
        self.__identity_application_service: IdentityApplicationService | None = None
        self.router.add_api_route('/register', self.register_user, methods=['POST'], response_model=UserDescriptorJson)
        self.router.add_api_route('/verify-email/{token}', self.verify_email, methods=['POST'])
        self.router.add_api_route('/token', self.token, methods=['POST'], response_model=Token)
        self.router.add_api_route('/token', self.refresh, methods=['PUT'], response_model=Token)
        self.router.add_api_route('/token', self.revoke, methods=['DELETE'])
        self.router.add_api_route('/forgot-password', self.forgot_password, methods=['POST'])
        self.router.add_api_route('/reset-password', self.reset_password, methods=['POST'])

    def register_user(self, request: RegisterUserRequest):
        self.__identity_application_service = self.__identity_application_service or \
                                              DIContainer.instance().resolve(IdentityApplicationService)
        dpo = self.__identity_application_service.register_user(RegisterUserCommand(
            request.email_address,
            request.password
        ))
        return UserDescriptorJson.from_(dpo)

    def verify_email(self, token: str):
        self.__identity_application_service = self.__identity_application_service or \
                                              DIContainer.instance().resolve(IdentityApplicationService)
        self.__identity_application_service.verify_email(token)

    def token(self, request: OAuth2PasswordRequest) -> Token:
        self.__identity_application_service = self.__identity_application_service or \
                                              DIContainer.instance().resolve(IdentityApplicationService)
        dpo = self.__identity_application_service.authenticate_user(AuthenticateUserCommand(request.email_address, request.password))
        return Token.generate(dpo)

    def refresh(self, current_user: UserDpo = Depends(get_current_active_user)) -> Token:
        return Token.generate(current_user)

    def revoke(self, current_user: UserDpo = Depends(get_current_active_user)) -> None:
        """ログアウト処理
        ・JWTを Redis から削除する
        """
        pass

    def forgot_password(self, request: ForgotPasswordRequest):
        self.__identity_application_service = self.__identity_application_service or \
                                              DIContainer.instance().resolve(IdentityApplicationService)
        self.__identity_application_service.forgot_password(ForgotPasswordCommand(request.email_address))

    def reset_password(self, request: ResetPasswordRequest):
        self.__identity_application_service = self.__identity_application_service or \
                                              DIContainer.instance().resolve(IdentityApplicationService)
        self.__identity_application_service.reset_password(ResetPasswordCommand(request.token, request.password))