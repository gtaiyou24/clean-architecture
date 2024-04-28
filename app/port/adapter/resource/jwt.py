import os

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt


class JWTEncoder:
    ALGORITHM = 'HS256'

    @staticmethod
    def encode(payload: dict) -> str:
        return jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), algorithm=JWTEncoder.ALGORITHM)

    @staticmethod
    def decode(token: str) -> dict:
        payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=[JWTEncoder.ALGORITHM])
        return payload


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not JWTEncoder.decode(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
