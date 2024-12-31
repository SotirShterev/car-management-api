from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database.database import get_db
from services.carservice import create_car, get_car_by_id, update_car, delete_car, get_all_cars
from dtos.carsdto import CreateCarDTO, UpdateCarDTO, ResponseCarDTO

router = APIRouter()

@router.post("", response_model=ResponseCarDTO)
def create(car_data: CreateCarDTO, db: Session = Depends(get_db)):
    return create_car(db, car_data)

@router.get("/{id}", response_model=ResponseCarDTO)
def get_by_id(id: int, db: Session = Depends(get_db)):
    return get_car_by_id(db, id)

@router.get("", response_model=list[ResponseCarDTO])
def get_cars(db: Session = Depends(get_db),carMake: Optional[str] = Query(None, description="Filter by car make"),
    garageId: Optional[int] = Query(None, description="Filter by garage id"),
    fromYear: Optional[int] = Query(None, description="Filter cars from year"),
    toYear: Optional[int] = Query(None, description="Filter cars to year")):
    return get_all_cars(db,carMake,garageId,fromYear,toYear)

@router.put("/{id}", response_model=ResponseCarDTO)
def update(id: int, car_data: UpdateCarDTO, db: Session = Depends(get_db)):
    return update_car(db, id, car_data)

@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    delete_car(db, id)
    return {"detail": "Resource deleted"}