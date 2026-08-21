from uuid import UUID

from pydantic import BaseModel, ConfigDict

class CompanySizeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    code:str
    name:str
    description: str | None = None
    is_active:bool