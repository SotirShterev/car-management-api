from datetime import date, datetime
from typing import List
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import func
from sqlalchemy.orm import Session
from models.models import Maintenance, Car, Garage
from dtos.maintenancedto import CreateMaintenanceDTO, UpdateMaintenanceDTO, ResponseMaintenanceDTO, \
    MonthlyRequestsReportDTO

def create_maintenance(db: Session, maintenance_data: CreateMaintenanceDTO) -> ResponseMaintenanceDTO:
    try:
        car = db.query(Car).filter(Car.id == maintenance_data.carId).first()
        garage = db.query(Garage).filter(Garage.id == maintenance_data.garageId).first()
        if not car:
            raise HTTPException(status_code=404, detail="Car not found")
        if not garage:
            raise HTTPException(status_code=404, detail="Garage not found")

        new_maintenance = Maintenance(
            car_id=maintenance_data.carId,
            garage_id=maintenance_data.garageId,
            serviceType=maintenance_data.serviceType,
            scheduledDate=maintenance_data.scheduledDate
        )
        db.add(new_maintenance)
        db.commit()
        db.refresh(new_maintenance)

        car_name = f"{car.make} {car.model}"

        return ResponseMaintenanceDTO(
            id=new_maintenance.id,
            carId=new_maintenance.car_id,
            carName=car_name,
            serviceType=new_maintenance.serviceType,
            scheduledDate=new_maintenance.scheduledDate,
            garageId=new_maintenance.garage_id,
            garageName=garage.name
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Bad request")

def get_maintenance_by_id(db: Session, maintenance_id: int) -> ResponseMaintenanceDTO:
    try:
        maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
        if not maintenance:
            raise HTTPException(status_code=404, detail="Resource not found")

        car = db.query(Car).filter(Car.id == maintenance.car_id).first()
        garage = db.query(Garage).filter(Garage.id == maintenance.garage_id).first()
        if not car or not garage:
            raise HTTPException(status_code=404, detail="Car or Garage not found")

        car_name = f"{car.make} {car.model}"

        return ResponseMaintenanceDTO(
            id=maintenance.id,
            carId=maintenance.car_id,
            carName=car_name,
            serviceType=maintenance.serviceType,
            scheduledDate=maintenance.scheduledDate,
            garageId=maintenance.garage_id,
            garageName=garage.name
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Bad request")

def update_maintenance(db: Session, maintenance_id: int, maintenance_data: UpdateMaintenanceDTO) -> ResponseMaintenanceDTO:
    try:
        maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
        if not maintenance:
            raise HTTPException(status_code=404, detail="Resource not found")

        for key, value in maintenance_data.model_dump(exclude_unset=True).items():
            if key == 'carId':
                maintenance.car_id = value
            elif key == 'garageId':
                maintenance.garage_id = value
            else:
                setattr(maintenance, key, value)
        db.commit()
        db.refresh(maintenance)

        car = db.query(Car).filter(Car.id == maintenance.car_id).first()
        garage = db.query(Garage).filter(Garage.id == maintenance.garage_id).first()
        if not car or not garage:
            raise HTTPException(status_code=404, detail="Car or Garage not found")

        car_name = f"{car.make} {car.model}"

        return ResponseMaintenanceDTO(
            id=maintenance.id,
            carId=maintenance.car_id,
            carName=car_name,
            serviceType=maintenance.serviceType,
            scheduledDate=maintenance.scheduledDate,
            garageId=maintenance.garage_id,
            garageName=garage.name
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Bad request")

def delete_maintenance(db: Session, maintenance_id: int) -> None:
    try:
        maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
        if not maintenance:
            raise HTTPException(status_code=404, detail="Resource not found")
        db.delete(maintenance)
        db.commit()
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Bad request")

def get_all_maintenances(db: Session,car_id: int = None,
    garage_id: int = None, ) -> list[ResponseMaintenanceDTO]:
    try:
        query = db.query(Maintenance)
        if car_id:
            query = query.filter(Maintenance.car_id == car_id)
        if garage_id:
            query = query.filter(Maintenance.garage_id == garage_id)
        maintenances = query.all()
        if not maintenances:
            raise HTTPException(status_code=404, detail="No maintenances found")

        response = []
        for maintenance in maintenances:
            car = db.query(Car).filter(Car.id == maintenance.car_id).first()
            garage = db.query(Garage).filter(Garage.id == maintenance.garage_id).first()
            if not car or not garage:
                raise HTTPException(status_code=404, detail=f"Car or Garage not found for maintenance ID {maintenance.id}")

            car_name = f"{car.make} {car.model}"

            response.append(ResponseMaintenanceDTO(
                id=maintenance.id,
                carId=maintenance.car_id,
                carName=car_name,
                serviceType=maintenance.serviceType,
                scheduledDate=maintenance.scheduledDate,
                garageId=maintenance.garage_id,
                garageName=garage.name
            ))
        return response
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Bad request")

def delete_all_maintenances(db: Session) -> None:
    try:
        db.query(Maintenance).delete()
        db.commit()
        print("All maintenances deleted successfully.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting maintenances: {str(e)}")

async def get_monthly_maintenance_report(
        db: Session,
        start_month: datetime,
        end_month: datetime,
        garage_id: int = None
) -> List[MonthlyRequestsReportDTO]:
    if start_month > end_month:
        raise ValueError("Start date cannot be later than end date.")

    months_in_range = []
    current_date = start_month
    while current_date <= end_month:
        months_in_range.append(current_date)
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)

    query = db.query(
        func.strftime('%Y-%m', Maintenance.scheduledDate).label('yearMonth'),
        func.count(Maintenance.id).label('requests')
    ).group_by(func.strftime('%Y-%m', Maintenance.scheduledDate))

    if garage_id:
        query = query.filter(Maintenance.garage_id == garage_id)
    query = query.filter(Maintenance.scheduledDate >= start_month)
    query = query.filter(Maintenance.scheduledDate <= end_month)
    grouped_data = query.all()

    report = []
    for month in months_in_range:
        month_str = month.strftime('%Y-%m')
        requests = next((item for item in grouped_data if item.yearMonth == month_str), None)
        report.append(MonthlyRequestsReportDTO(
            yearMonth=month_str,
            requests=requests.requests if requests else 0
        ))
    return report