from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from services.maintenanceservice import create_maintenance, get_maintenance_by_id, update_maintenance, \
    delete_maintenance, get_all_maintenances, delete_all_maintenances,get_monthly_maintenance_report
from dtos.maintenancedto import CreateMaintenanceDTO, UpdateMaintenanceDTO, ResponseMaintenanceDTO, \
    MonthlyRequestsReportDTO

router = APIRouter()

@router.post("", response_model=ResponseMaintenanceDTO)
def create(maintenance_data: CreateMaintenanceDTO, db: Session = Depends(get_db)):
    return create_maintenance(db, maintenance_data)

@router.get("&quot;/{id}&quot;", response_model=ResponseMaintenanceDTO)
def get_by_id(id: int, db: Session = Depends(get_db)):
    return get_maintenance_by_id(db, id)

@router.get("", response_model=list[ResponseMaintenanceDTO])
def get_maintenances(db: Session = Depends(get_db),
                     carId: Optional[int] = Query(None, description="Filter by car"),
                     garageId: Optional[int] = Query(None, description="Filter by garage")):
    return get_all_maintenances(db,carId,garageId)

@router.put("/{id}", response_model=ResponseMaintenanceDTO)
def update(id: int, maintenance_data: UpdateMaintenanceDTO, db: Session = Depends(get_db)):
    return update_maintenance(db, id, maintenance_data)

@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    delete_maintenance(db, id)
    return {"detail": "Resource deleted"}

@router.delete("")
def delete_maintenances(db:Session = Depends(get_db)):
    return delete_all_maintenances(db)

@router.get("/monthlyRequestsReport", response_model=List[MonthlyRequestsReportDTO])
async def monthly_requests_report(garageId: int = Query(...), startMonth: str = Query(...), endMonth: str = Query(...),
                                  db: Session = Depends(get_db)):
        start_month_dt = datetime.strptime(startMonth, "%Y-%m")
        end_month_dt = datetime.strptime(endMonth, "%Y-%m")
        report = await get_monthly_maintenance_report(db, start_month_dt, end_month_dt, garageId)
        return report


