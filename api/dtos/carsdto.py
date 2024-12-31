from pydantic import BaseModel, Field
from typing import Optional, List
from dtos.garagedto import ResponseGarageDTO

class CreateCarDTO(BaseModel):
    make: str = Field(...)
    model: str = Field(...)
    productionYear: int = Field(...)
    licensePlate: str = Field(...)
    garageIds: List[Optional[int]] = Field(None)

class UpdateCarDTO(BaseModel):
    make: Optional[str] = Field(None)
    model: Optional[str] = Field(None)
    productionYear: Optional[int] = Field(None)
    licensePlate: Optional[str] = Field(None)
    garageIds: List[Optional[int]] = Field(None)

class ResponseCarDTO(BaseModel):
    id: int
    make: str
    model: str
    productionYear: int
    licensePlate: str
    garages: List[Optional[ResponseGarageDTO]]

    class Config:
        from_attributes = True