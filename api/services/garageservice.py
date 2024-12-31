from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session
from models.models import Garage, Maintenance
from dtos.garagedto import CreateGarageDTO, UpdateGarageDTO, ResponseGarageDTO, GarageDailyAvailabilityReportDTO

def create_garage(db: Session, garage_data: CreateGarageDTO) -> ResponseGarageDTO:
    try:
        new_garage = Garage(**garage_data.model_dump())
        db.add(new_garage)
        db.commit()
        db.refresh(new_garage)
        return ResponseGarageDTO.model_validate(new_garage)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Bad request")

def get_garage_by_id(db: Session, garage_id: int) -> ResponseGarageDTO:
    try:
        garage = db.query(Garage).filter(Garage.id == garage_id).first()
        if not garage:
            raise HTTPException(status_code=404, detail="Resource not found")
        return ResponseGarageDTO.model_validate(garage)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Bad request")

def update_garage(db: Session, garage_id: int, garage_data: UpdateGarageDTO) -> ResponseGarageDTO:
    try:
        garage = db.query(Garage).filter(Garage.id == garage_id).first()
        if not garage:
            raise HTTPException(status_code=404, detail="Resource not found")

        for key, value in garage_data.model_dump(exclude_unset=True).items():
            setattr(garage, key, value)
        db.commit()
        db.refresh(garage)
        return ResponseGarageDTO.model_validate(garage)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Bad request")

def delete_garage(db: Session, garage_id: int) -> None:
    try:
        garage = db.query(Garage).filter(Garage.id == garage_id).first()
        if not garage:
            raise HTTPException(status_code=404, detail="Resource not found")
        db.delete(garage)
        db.commit()
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Bad request")

def get_all_garages(db: Session,city: Optional[str] = None) -> list[ResponseGarageDTO]:
    try:
        query = db.query(Garage)
        if city:
            query = query.filter(Garage.city.ilike(f"%{city}%"))
        garages = query.all()

        return [ResponseGarageDTO.model_validate(garage) for garage in garages]
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Bad request")

def generate_daily_availability_report(db: Session,
                                       garage_id: int, start_date: str, end_date: str) -> list[GarageDailyAvailabilityReportDTO]:
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid date format. Received start_date: {start_date}, end_date: {end_date}")

    if start_date > end_date:
        raise HTTPException(status_code=400, detail=f"Invalid date range. Start date {start_date} is after end date {end_date}.")

    garage = db.query(Garage).filter(Garage.id == garage_id).first()
    if not garage:
        raise HTTPException(status_code=404, detail=f"Garage with id {garage_id} not found.")

    dates = [(start_date + timedelta(days=i)) for i in range((end_date - start_date).days + 1)]

    report = []
    for date in dates:
        maintenance_count = (db.query(Maintenance)
            .filter(Maintenance.garage_id == garage_id,Maintenance.scheduledDate == date.date())
            .count()

        )
        free_capacity = garage.capacity - maintenance_count
        report.append(
            GarageDailyAvailabilityReportDTO(
                date=date.strftime("%Y-%m-%d"),
                requests=maintenance_count,
                availableCapacity=free_capacity
            )
        )
    return report
