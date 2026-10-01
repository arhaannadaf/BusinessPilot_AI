from uuid import UUID
from pydantic import BaseModel, ConfigDict

class CountryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    code: str
    code_3: str
    name: str
    is_active:bool