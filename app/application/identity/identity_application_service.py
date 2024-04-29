from __future__ import annotations

import os

from injector import singleton, inject

from application import transactional
from application.identity.command import (
    RegisterUserCommand,
    AuthenticateUserCommand,
    ForgotPasswordCommand,
    ResetPasswordCommand, DeleteUserCommand,
)
from application.identity.dpo import UserDpo
from domain.model.mail import MailDeliveryService, EmailAddress
from domain.model.user import UserRepository, User
from exception import SystemException, ErrorCode


@singleton
class IdentityApplicationService:
    @inject
    def __init__(
        self,
        user_repository: UserRepository,
        mail_delivery_service: MailDeliveryService,
    ):
        self.__user_repository = user_repository
        self.__mail_delivery_service = mail_delivery_service

    @transactional
    def provision_user(self, command: RegisterUserCommand) -> UserDpo:
        """ユーザー仮登録"""
        user = User.provision(
            self.__user_repository.next_identity(),
            EmailAddress(command.email_address),
            command.plain_password
        )

        if self.__user_repository.user_with_email_address(user.email_address):
            raise SystemException(
                ErrorCode.REGISTER_USER_ALREADY_EXISTS, "ユーザー登録に失敗しました。"
            )

        # メールアドレスが正しいか検証するためにトークンを発行
        token = user.generate_verification_token()
        self.__user_repository.add(user)

        self.__mail_delivery_service.send(
            user.email_address,
            "メールアドレスを確認します",
            f"""
            <html>
            <body>
                <h1>メールアドレスの確認をします</h1>
                <a href="{os.getenv('FRONTEND_URL')}/auth/new-verification?token={token.value}">こちらをクリックしてください。</a>
            </body>
            </html>
            """,
        )

        return UserDpo(user)

    @transactional
    def verify_email(self, verification_token_value: str) -> None:
        """
        新規登録時に発行されたトークンを検証する。
        このメソッドはユーザーの新規登録時にメール送信されたトークンをもとにユーザーが正しいメールアドレスを入力したか検証するためのものです。
        """
        user = self.__user_repository.user_with_token(verification_token_value)
        if user is None or user.token_with(verification_token_value).has_expired():
            raise SystemException(
                ErrorCode.VALID_TOKEN_DOES_NOT_EXISTS,
                f"{verification_token_value}は無効なトークンです。",
            )

        user.verified()

        self.__user_repository.add(user)

    def authenticate_user(self, command: AuthenticateUserCommand) -> UserDpo | None:
        """ユーザー認証"""
        email_address = EmailAddress(command.email_address)
        user = self.__user_repository.user_with_email_address(email_address)

        # 該当ユーザーが存在するか、パスワードは一致しているか
        if user is None or not user.verify_password(command.password):
            raise SystemException(
                ErrorCode.LOGIN_BAD_CREDENTIALS, "ユーザーが見つかりませんでした。"
            )

        # メールアドレス検証が終わっていない場合は、確認メールを再送信する
        if not user.is_verified():
            token = user.generate_verification_token()
            self.__user_repository.add(user)
            self.__mail_delivery_service.send(
                user.email_address,
                "メールアドレスを確認します",
                f"""
                <html>
                <body>
                    <h1>メールアドレスの確認をします</h1>
                    <a href="{os.getenv('FRONTEND_URL')}/auth/new-verification?token={token.value}">こちらをクリックしてください。</a>
                </body>
                </html>
                """,
            )
            return None

        return UserDpo(user)

    @transactional
    def authenticate_github_user(self, command: AuthenticateUserCommand) -> UserDpo:
        email_address = EmailAddress(command.email_address)
        user = self.__user_repository.user_with_email_address(email_address)

        if user is not None:
            # すでにユーザーが存在する場合は、認証完了とする
            return UserDpo(user)

        user = User.provision(self.__user_repository.next_identity(), email_address, None)
        user.verified()
        self.__user_repository.add(user)
        return UserDpo(user)

    def user(self, email_address: str) -> UserDpo | None:
        user = self.__user_repository.user_with_email_address(
            EmailAddress(email_address)
        )
        if user is None:
            return None
        return UserDpo(user)

    @transactional
    def forgot_password(self, command: ForgotPasswordCommand) -> None:
        """メールアドレス指定でパスワードリセットメールを送信する"""
        email_address = EmailAddress(command.email_address)
        user = self.__user_repository.user_with_email_address(email_address)
        if user is None:
            raise SystemException(
                ErrorCode.USER_DOES_NOT_EXISTS,
                f"{email_address.value} に紐づくユーザーが見つからなかったため、パスワードリセットメールを送信できませんでした。",
            )

        token = user.generate_password_reset_token()
        self.__mail_delivery_service.send(
            user.email_address,
            "パスワードのリセット",
            f"""
            <html>
            <body>
                <h1>パスワードをリセット</h1>
                <a href="{os.getenv('FRONTEND_URL')}/auth/new-password?token={token.value}">こちらをクリックしてください。</a>
            </body>
            </html>
            """,
        )
        self.__user_repository.add(user)

    @transactional
    def reset_password(self, command: ResetPasswordCommand) -> None:
        """新しく設定したパスワードとパスワードリセットトークン指定で新しいパスワードに変更する"""
        user = self.__user_repository.user_with_token(command.reset_token)
        if user is None or user.token_with(command.reset_token).has_expired():
            raise SystemException(
                ErrorCode.VALID_TOKEN_DOES_NOT_EXISTS,
                f"指定したトークン {command.reset_token} は無効なのでパスワードをリセットできません。",
            )

        user.reset_password(command.password, command.reset_token)

        self.__user_repository.add(user)

    @transactional
    def delete(self, command: DeleteUserCommand) -> None:
        self.__user_repository.remove(command.user)
