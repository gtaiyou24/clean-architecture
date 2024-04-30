from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    FROM_MAIL_ADDRESS: str = 'hello@clean-architecture.com'
    FRONTEND_URL: str = 'http://localhost:3000'


class LocalSettings(AppSettings):
    pass


class ProductionSettings(AppSettings):
    pass
