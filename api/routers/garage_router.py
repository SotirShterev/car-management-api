from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database.database import get_db
from services.garageservice import create_garage, get_garage_by_id, update_garage, delete_garage, get_all_garages, \
    generate_daily_availability_report
from dtos.garagedto import CreateGarageDTO, UpdateGarageDTO, ResponseGarageDTO, GarageDailyAvailabilityReportDTO

router = APIRouter()

@router.post("", response_model=ResponseGarageDTO)
def create(garage_data: CreateGarageDTO, db: Session = Depends(get_db)):
    return create_garage(db, garage_data)

@router.get("&quot;/{id}&quot;", response_model=ResponseGarageDTO)
def get_by_id(id: int, db: Session = Depends(get_db)):
    return get_garage_by_id(db, id)

@router.get("", response_model=list[ResponseGarageDTO])
def get_garages(db: Session = Depends(get_db),city: Optional[str] = Query(None, description="Filter by city")):
    return get_all_garages(db,city)

@router.put("/{id}", response_model=ResponseGarageDTO)
def update(id: int, garage_data: UpdateGarageDTO, db: Session = Depends(get_db)):
    return update_garage(db, id, garage_data)

@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    delete_garage(db, id)
    return {"detail": "Garage deleted"}

@router.get("/dailyAvailabilityReport", response_model=list[GarageDailyAvailabilityReportDTO])
def daily_availability_report(garageId: int, startDate: str, endDate: str, db: Session = Depends(get_db)):
    return generate_daily_availability_report(db, garageId, startDate, endDate)
