from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CurrencyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    code: str
    name: str
    symbol: str | None = None
    is_active: bool