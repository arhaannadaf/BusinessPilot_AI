from app.modules.reference.country.repository import CountryRepository
from app.modules.reference.country.schema import CountryResponse

class CountryService:
        
    def __init__(
            self,
            respository: CountryRepository

        ):
        self.respository = respository
    async def list_countries(
            self,
            *,
            is_active: bool | None = True

    ) -> list[CountryResponse]:

        countries = await self.respository.list(
            is_active = is_active
        )

        return [
            CountryResponse.model_validate(country)
            for country in countries
        ]