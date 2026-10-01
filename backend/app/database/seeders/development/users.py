from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.identity.organization import Organization
from app.database.models.identity.role import Role
from app.database.models.identity.user import User


async def seed_user(session: AsyncSession) -> None:

    organization = await session.scalar(
        select(Organization).where(
            Organization.domain == "businesspilot.ai"
        )
    )

    if not organization:
        raise ValueError(
            "BusinessPilot organization not found."
        )

    role = await session.scalar(
        select(Role).where(
            Role.name == "Admin"
        )
    )

    if not role:
        raise ValueError(
            "Admin role not found."
        )

    existing_user = await session.scalar(
        select(User).where(
            User.username == "engine_test_user"
        )
    )

    if existing_user:
        print("Development test user already exists.")
        return

    user = User(
        organization_id=organization.id,
        role_id=role.id,
        first_name="Engine",
        Last_name="Test",
        username="engine_test_user",
        email="engine_test@businesspilot.ai",
        password_hash="development-only-password",
        is_active=True,
    )

    session.add(user)

    print("Development test user created.")