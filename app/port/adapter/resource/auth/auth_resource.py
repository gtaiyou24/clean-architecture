from __future__ import annotations

from di import DIContainer
from fastapi import APIRouter, Depends

from application.identity import IdentityApplicationService
from application.identity.command import (
    RegisterUserCommand,
    AuthenticateUserCommand,
    ForgotPasswordCommand,
    ResetPasswordCommand, DeleteUserCommand, RefreshCommand, RevokeCommand,
)
from application.identity.dpo import UserDpo
from port.adapter.resource import APIResource
from port.adapter.resource.auth.request import (
    RegisterUserRequest,
    OAuth2PasswordRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from port.adapter.resource.auth.response import UserDescriptorJson, TokenJson
from port.adapter.resource.dependency import get_current_active_user


class AuthResource(APIResource):
    router = APIRouter(prefix="/auth", tags=["Auth"])

    def __init__(self):
        self.__identity_application_service: IdentityApplicationService | None = None
        self.router.add_api_route(
            "/register",
            self.register_user,
            methods=["POST"],
            response_model=UserDescriptorJson,
            name='ユーザーを登録'
        )
        self.router.add_api_route(
            "/verify-email/{token}", self.verify_email, methods=["POST"], name='メールアドレスを確認'
        )
        self.router.add_api_route(
            "/token", self.token, methods=["POST"], response_model=TokenJson, name='トークンを発行'
        )
        self.router.add_api_route(
            "/token", self.refresh, methods=["PUT"], response_model=TokenJson, name='トークンを更新'
        )
        self.router.add_api_route("/token", self.revoke, methods=["DELETE"], name='トークンを削除')
        self.router.add_api_route(
            "/forgot-password", self.forgot_password, methods=["POST"], name='パスワードを忘れた'
        )
        self.router.add_api_route(
            "/reset-password", self.reset_password, methods=["POST"], name='パスワードをリセット'
        )
        self.router.add_api_route(
            "/unregister", self.unregister, methods=["DELETE"], name='ユーザーを削除'
        )

    @property
    def identity_application_service(self) -> IdentityApplicationService:
        self.__identity_application_service = (
                self.__identity_application_service
                or DIContainer.instance().resolve(IdentityApplicationService)
        )
        return self.__identity_application_service

    def register_user(self, request: RegisterUserRequest):
        command = RegisterUserCommand(request.email_address, request.password)
        dpo = self.identity_application_service.provision_user(command)
        return UserDescriptorJson.from_(dpo)

    def verify_email(self, token: str):
        self.identity_application_service.verify_email(token)

    def token(self, request: OAuth2PasswordRequest) -> TokenJson:
        command = AuthenticateUserCommand(request.email_address, request.password)
        dpo = self.identity_application_service.authenticate_user(command)
        return TokenJson.generate(dpo)

    def refresh(
        self, current_user: UserDpo = Depends(get_current_active_user)
    ) -> TokenJson:
        command = RefreshCommand.from_(current_user)
        dpo = self.identity_application_service.refresh(command)
        return TokenJson.generate(dpo)

    def revoke(self, current_user: UserDpo = Depends(get_current_active_user)) -> None:
        command = RevokeCommand.from_(current_user)
        self.identity_application_service.revoke(command)

    def forgot_password(self, request: ForgotPasswordRequest):
        command = ForgotPasswordCommand(request.email_address)
        self.identity_application_service.forgot_password(command)

    def reset_password(self, request: ResetPasswordRequest):
        command = ResetPasswordCommand(request.token, request.password)
        self.identity_application_service.reset_password(command)

    def unregister(
            self, current_user: UserDpo = Depends(get_current_active_user)
    ) -> None:
        command = DeleteUserCommand(current_user.user)
        self.identity_application_service.delete(command)
