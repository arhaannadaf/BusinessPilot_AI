from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.database.models.identity.organization import Organization
from app.database.models.identity.user import User
from app.database.session import get_db
from app.modules.identity.schemas import CurrentActor

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_actor(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db),
) -> CurrentActor:
    try:
        user_id: UUID = decode_access_token(token)
    except (JWTError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    result = await session.execute(
        select(User, Organization)
        .join(Organization, Organization.id == User.organization_id)
        .where(
            User.id == user_id,
            User.is_active.is_(True),
            Organization.is_active.is_(True),
        )
    )
    row = result.one_or_none()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated user or organization is inactive.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user, _organization = row
    return CurrentActor(
        user_id=user.id,
        organization_id=user.organization_id,
        role_id=user.role_id,
    )
