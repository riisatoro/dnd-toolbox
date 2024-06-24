from datetime import datetime, timedelta
from typing import Union, Annotated
import os

import jwt
from fastapi import Cookie, Depends

from database.connection import session as dbsession
from database.models.users import User
from exceptions.authorization import NotAuthorizedError


SECRET_KEY = os.getenv("SECRET_KEY", "my_secret")
JWT_EXPIRATION_SEC = int(os.getenv("JWT_EXPIRATION_SEC", 3600))

ALGORITHM = "HS256"
AUDIENCE = "aud:access"
AUDIENCE_REFRESH = "aud:refresh"
TOKEN_KEY = "session_id"


class JWTSecurity:
    @staticmethod
    def create_token(user_id: int) -> str:
        payload_access = {
            "uid": user_id,
            "aud": [AUDIENCE],
            "exp": datetime.now() + timedelta(seconds=JWT_EXPIRATION_SEC),
        }
        return jwt.encode(payload_access, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def validate_token(session: Union[str, None] = Cookie(None)):
        if not session:
            raise NotAuthorizedError
        try:
            payload = jwt.decode(
                session,
                SECRET_KEY,
                audience=AUDIENCE,
                algorithms=[ALGORITHM]
            )
            user = dbsession.query(User).filter(User.id == payload["uid"]).first()
            if not user:
                raise NotAuthorizedError
            return user
        except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
            raise NotAuthorizedError


AuthDepends = Annotated[bool, Depends(JWTSecurity.validate_token)]
