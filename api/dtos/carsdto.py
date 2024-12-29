from pydantic import BaseModel, Field
from typing import Optional, List
from dtos.garagedto import ResponseGarageDTO

class CreateCarDTO(BaseModel):
    make: str = Field(..., min_length=1)
    model: str = Field(..., min_length=1)
    productionYear: int = Field(..., ge=1886)
    licensePlate: str = Field(..., min_length=1)
    garageIds: List[Optional[int]] = Field(None)

class UpdateCarDTO(BaseModel):
    make: Optional[str] = Field(None, min_length=1)
    model: Optional[str] = Field(None, min_length=1)
    productionYear: Optional[int] = Field(None, ge=1886)
    licensePlate: Optional[str] = Field(None, min_length=1)
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