from datetime import datetime, timedelta, timezone

from jose import jwt

from settings import Settings

ALGORITHM = "HS256"


def create_access_token(data: dict, expires_minutes: int = 60) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    return jwt.encode(to_encode, Settings().JWT_SECRET, algorithm=ALGORITHM)
