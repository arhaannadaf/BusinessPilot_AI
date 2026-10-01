from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, HttpUrl


class CompanyBase(BaseModel):
    name:str 
    legal_name: str | None = None
    website: HttpUrl | None = None
    description: str | None = None

    industry_id: UUID | None = None
    company_size_id: UUID | None = None
    company_status_id: UUID | None = None
    country_id: UUID | None = None

    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    address_line_1: str | None = None
    address_line_2: str | None = None

    employee_count: int | None = None
    annual_revenue: Decimal | None =None
    founded_year: int | None = None

    email: EmailStr | None = None
    phone: str | None = None
    linkedin_url: HttpUrl | None = None

    is_customer: bool = False
    is_partner: bool = False
    is_active: bool = True

class CompanyCreate(CompanyBase):
    organization_id: UUID

class CompanyUpdate(BaseModel):
        model_config = ConfigDict(extra="forbid")

        name: str | None = None
        legal_name: str | None = None
        website: HttpUrl | None = None
        description: str | None = None

        industry_id: UUID | None = None
        company_size_id: UUID | None = None
        company_status_id: UUID | None = None
        country_id: UUID | None = None

        city: str | None = None
        state: str | None = None
        postal_code: str | None = None
        address_line_1: str | None = None
        address_line_2: str | None = None
        
        employee_count: int | None = None
        annual_revenue: Decimal | None =None
        founded_year: int | None = None
      
        email: EmailStr | None = None
        phone: str | None = None
        linkedin_url: HttpUrl | None = None
      
        is_customer: bool = False
        is_partner: bool = False
        is_active: bool = True

class CompanyResponse(BaseModel):
     model_config = ConfigDict(from_attributes=True)
     id: UUID 
     organization_id: UUID

     name: str
     legal_name: str | None = None
     website: HttpUrl | None = None
     description: str | None = None

     industry_id: UUID | None = None
     company_size_id: UUID | None = None
     company_status_id: UUID | None = None
     country_id: UUID | None = None

     city: str | None = None
     state: str |None = None
     postal_code: str | None = None
     address_line_1: str | None = None
     address_line_2: str | None = None

     employee_count: int | None = None
     annual_revenue: Decimal | None = None
     founded_year: int | None = None

     email: EmailStr | None = None
     phone: str | None = None
     linkedin_url: HttpUrl | None = None

     is_customer:bool
     is_partner:bool
     is_active:bool

     created_at: datetime
     updated_at: datetime

class CompanyListResponse(BaseModel):
     items: list[CompanyResponse]

     page:int
     page_size:int
     total: int
     pages:int

     has_next:bool
     has_previous:bool