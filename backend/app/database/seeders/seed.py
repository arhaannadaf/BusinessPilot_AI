import asyncio
from app.database.session import SessionLocal
from app.database.seeders.base import seed_model

# Models
from app.database.models.reference.industry import Industry
from app.database.models.reference.company_status import CompanyStatus
from app.database.models.reference.company_size import CompanySize
from app.database.models.reference.country import Country
from app.database.models.reference.currency import Currency

from app.database.models.identity.organization import Organization
# Seed Data
from app.database.seeders.reference.industries import INDUSTRIES
from app.database.seeders.reference.company_statuses import COMPANY_STATUSES
from app.database.seeders.reference.company_sizes import COMPANY_SIZES
from app.database.seeders.reference.countries import COUNTRIES
from app.database.seeders.reference.currencies import CURRENCIES

from app.database.seeders.development.organizations import seed_organizations as ORGANIZATIONS
async def run_seed():
    async with SessionLocal() as session:

        try:
            await seed_model(session, Industry, INDUSTRIES)
            await seed_model(session, CompanyStatus, COMPANY_STATUSES)
            await seed_model(session, CompanySize, COMPANY_SIZES)
            await seed_model(session, Country, COUNTRIES)
            await seed_model(session, Currency, CURRENCIES)

            await ORGANIZATIONS(session)

            await session.commit()

            print("✅ Database seeded successfully.")

        except Exception:
            await session.rollback()
            raise

if __name__ == "__main__":
    asyncio.run(run_seed())