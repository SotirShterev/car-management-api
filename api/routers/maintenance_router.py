from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from services.maintenanceservice import create_maintenance, get_maintenance_by_id, update_maintenance, \
    delete_maintenance, get_all_maintenances, delete_all_maintenances
from dtos.maintenancedto import CreateMaintenanceDTO, UpdateMaintenanceDTO, ResponseMaintenanceDTO

router = APIRouter()

@router.post("", response_model=ResponseMaintenanceDTO)
def create(maintenance_data: CreateMaintenanceDTO, db: Session = Depends(get_db)):
    return create_maintenance(db, maintenance_data)

@router.get("/{id}", response_model=ResponseMaintenanceDTO)
def get_by_id(id: int, db: Session = Depends(get_db)):
    return get_maintenance_by_id(db, id)

@router.get("", response_model=list[ResponseMaintenanceDTO])
def get_maintenances(db: Session = Depends(get_db)):
    return get_all_maintenances(db)

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


