from datetime import datetime, timedelta
from typing import Union, Annotated
import os

import jwt
from fastapi import Header, Depends

from database.connection import session
from database.models.users import User
from exceptions.authorization import NotAuthorizedError


SECRET_KEY = os.getenv("SECRET_KEY", "my_secret")
JWT_EXPIRATION_SEC = int(os.getenv("JWT_EXPIRATION_SEC", 3600))
JWT_REFRESH_EXPIRATION_SEC = int(os.getenv("JWT_REFRESH_EXPIRATION_SEC", 21700))
ALGORITHM = "HS256"
AUDIENCE = "aud:access"
AUDIENCE_REFRESH = "aud:refresh"
TOKEN_KEY = "session_id"


class JWTSecurity:
    @staticmethod
    def create_tokens(user_id: int) -> dict:
        payload_access = {
            "uid": user_id,
            "aud": [AUDIENCE],
            "exp": datetime.now() + timedelta(seconds=JWT_EXPIRATION_SEC),
        }
        payload_refresh = {
            "uid": user_id,
            "aud": [AUDIENCE_REFRESH],
            "exp": datetime.now() + timedelta(seconds=JWT_REFRESH_EXPIRATION_SEC),
        }
        access = jwt.encode(payload_access, SECRET_KEY, algorithm=ALGORITHM)
        refresh = jwt.encode(payload_refresh, SECRET_KEY, algorithm=ALGORITHM)
        return {"access": access, "refresh": refresh}

    @staticmethod
    def validate_token(X_ACCESS_TOKEN: Union[str, None] = Header(None)):
        if not X_ACCESS_TOKEN:
            raise NotAuthorizedError
        try:
            payload = jwt.decode(
                X_ACCESS_TOKEN,
                SECRET_KEY,
                audience=AUDIENCE,
                algorithms=[ALGORITHM]
            )
            user = session.query(User).filter(User.id == payload["uid"]).first()
            if not user:
                raise NotAuthorizedError
            return user
        except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
            raise NotAuthorizedError

    @staticmethod
    def refresh_token(refresh_token):
        try:
            payload = jwt.decode(
                refresh_token,
                SECRET_KEY,
                audience=AUDIENCE_REFRESH,
                algorithms=[ALGORITHM]
            )
            user = session.query(User).filter(User.id == payload["uid"]).first()
            if not user:
                raise NotAuthorizedError
            return JWTSecurity.create_tokens(user.id)
        except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
            return None


AuthDepends = Annotated[bool, Depends(JWTSecurity.validate_token)]
