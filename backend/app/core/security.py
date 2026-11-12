from datetime import UTC, datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt
from pwdlib import PasswordHash

from app.core.config.settings import settings

password_context = PasswordHash.recommended()


def verify_password(plain_password: str, password_hash: str) -> bool:
    return password_context.verify(plain_password, password_hash)


def hash_password(password: str) -> str:
    return password_context.hash(password)


def create_access_token(user_id: UUID) -> str:
    expires_at = datetime.now(UTC) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {"sub": str(user_id), "exp": expires_at}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> UUID:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        subject = payload.get("sub")
        if not subject:
            raise ValueError("Access token has no subject.")
        return UUID(subject)
    except (JWTError, ValueError) as exc:
        raise ValueError("Invalid access token.") from exc