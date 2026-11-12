from uuid import UUID

from pydantic import BaseModel


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: UUID
    organization_id: UUID


class CurrentActor(BaseModel):
    user_id: UUID
    organization_id: UUID
    role_id: UUID
