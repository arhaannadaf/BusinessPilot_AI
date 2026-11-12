from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, verify_password
from app.database.models.identity.user import User
from app.database.session import get_db
from app.modules.identity.schemas import AccessTokenResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=AccessTokenResponse)
async def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db),
) -> AccessTokenResponse:
    user = await session.scalar(
        select(User).where(
            User.username == credentials.username,
            User.is_active.is_(True),
        )
    )

    if user is None or not verify_password(
        credentials.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return AccessTokenResponse(
        access_token=create_access_token(user.id),
        user_id=user.id,
        organization_id=user.organization_id,
    )
