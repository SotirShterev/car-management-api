from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from services.garageservice import create_garage, get_garage_by_id, update_garage, delete_garage,get_all_garages
from dtos.garagedto import CreateGarageDTO, UpdateGarageDTO, ResponseGarageDTO

router = APIRouter()

@router.post("", response_model=ResponseGarageDTO)
def create(garage_data: CreateGarageDTO, db: Session = Depends(get_db)):
    return create_garage(db, garage_data)

@router.get("/{id}", response_model=ResponseGarageDTO)
def get_by_id(id: int, db: Session = Depends(get_db)):
    return get_garage_by_id(db, id)

@router.get("", response_model=list[ResponseGarageDTO])
def get_garages(db: Session = Depends(get_db)):
    return get_all_garages(db)

@router.put("/{id}", response_model=ResponseGarageDTO)
def update(id: int, garage_data: UpdateGarageDTO, db: Session = Depends(get_db)):
    return update_garage(db, id, garage_data)

@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    delete_garage(db, id)
    return {"detail": "Resource deleted"}