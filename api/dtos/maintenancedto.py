from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class CreateMaintenanceDTO(BaseModel):
    garageId: int = Field(...)
    carId: int = Field(...)
    serviceType: str = Field(..., min_length=1)
    scheduledDate: date = Field(...)

class UpdateMaintenanceDTO(BaseModel):
    carId: Optional[int] = Field(None)
    serviceType: Optional[str] = Field(None, min_length=1)
    scheduledDate: Optional[date] = Field(None)
    garageId: Optional[int] = Field(None)

class ResponseMaintenanceDTO(BaseModel):
    id: int
    carId: int = Field(...)
    carName: str
    serviceType: str
    scheduledDate: date
    garageId: int = Field(...)
    garageName: str

    class Config:
        from_attributes = True