from di import DIContainer
from fastapi import HTTPException, Depends, status
from jose import JWTError

from application.identity import IdentityApplicationService
from application.identity.dpo import UserDpo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserDpo:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = JWTEncoder.decode(token)
        email_address: str = payload.get("sub")
        if email_address is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    application_service = DIContainer.instance().resolve(IdentityApplicationService)
    dpo = application_service.user(email_address)
    if dpo is None:
        raise credentials_exception
    return dpo


async def get_current_active_user(current_user: UserDpo = Depends(get_current_user)) -> UserDpo:
    if current_user.user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
