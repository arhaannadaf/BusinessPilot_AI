import asyncio

from sqlalchemy import select
from pwdlib import PasswordHash

from app.database.session import SessionLocal
from app.database.models.identity.user import User
from app.database.models.identity.organization import Organization
from app.database.models.identity.role import Role


password_hash = PasswordHash.recommended()


async def create_test_user():

    async with SessionLocal() as session:

        # Find organization
        organization = await session.scalar(
            select(Organization).where(
                Organization.domain == "businesspilot.ai"
            )
        )

        if organization is None:
            raise ValueError(
                "BusinessPilot organization not found."
            )

        # Find Admin role
        role = await session.scalar(
            select(Role).where(
                Role.name == "Admin"
            )
        )

        if role is None:
            raise ValueError(
                "Admin role not found."
            )

        # Prevent duplicate test user
        existing = await session.scalar(
            select(User).where(
                User.username == "dev_admin"
            )
        )

        if existing:
            print("Temporary development user already exists.")
            print("User ID:", existing.id)
            print("Organization ID:", existing.organization_id)
            return

        user = User(
            organization_id=organization.id,
            role_id=role.id,
            first_name="Development",
            Last_name="Admin",
            username="dev_admin",
            email="dev_admin@businesspilot.local",
            password_hash=password_hash.hash("DevAdmin@123"),
            phone=None,
            is_active=True,
        )

        session.add(user)

        await session.commit()
        await session.refresh(user)

        print("\nTemporary development user created.")
        print("User ID:", user.id)
        print("Organization ID:", user.organization_id)
        print("Role ID:", user.role_id)
        print("Username:", user.username)
        print("Email:", user.email)


if __name__ == "__main__":
    asyncio.run(create_test_user())