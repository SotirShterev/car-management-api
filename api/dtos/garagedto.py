from pydantic import BaseModel, Field
from typing import Optional

class GarageDailyAvailabilityReportDTO(BaseModel):
    date: str = Field(...)
    requests: int = Field(...)
    availableCapacity: int = Field(...)

class CreateGarageDTO(BaseModel):
    name: str = Field(...)
    location: str = Field(...)
    city: str = Field(...)
    capacity: int = Field(..., ge=1)

class UpdateGarageDTO(BaseModel):
    name: Optional[str] = Field(None)
    location: Optional[str] = Field(None)
    capacity: Optional[int] = Field(None, ge=1)
    city: Optional[str] = Field(None)

class ResponseGarageDTO(BaseModel):
    id: int
    name: str
    location : str
    city: str
    capacity: int

    class Config:
        from_attributes = True



