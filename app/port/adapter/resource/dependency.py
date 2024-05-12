from di import DIContainer
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from application.identity import IdentityApplicationService
from application.identity.dpo import UserDpo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserDpo:
    application_service = DIContainer.instance().resolve(IdentityApplicationService)
    dpo = application_service.user_with_token(token)
    if dpo is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return dpo


async def get_current_active_user(
    current_user: UserDpo = Depends(get_current_user),
) -> UserDpo:
    if current_user.user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
