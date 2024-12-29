from typing import Optional

from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session
from models.models import Car, Garage
from dtos.carsdto import CreateCarDTO, UpdateCarDTO, ResponseCarDTO

def create_car(db: Session, car_data: CreateCarDTO) -> ResponseCarDTO:
    try:
        new_car = Car(
            make=car_data.make,
            model=car_data.model,
            productionYear=car_data.productionYear,
            licensePlate=car_data.licensePlate
        )
        if car_data.garageIds:
            for garage_id in car_data.garageIds:
                garage = db.query(Garage).filter(Garage.id == garage_id).first()
                if garage:
                    new_car.garages.append(garage)
        db.add(new_car)
        db.commit()
        db.refresh(new_car)
        return ResponseCarDTO.model_validate(new_car)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Bad request")

def get_car_by_id(db: Session, car_id: int) -> ResponseCarDTO:
    try:
        car = db.query(Car).filter(Car.id == car_id).first()
        if not car:
            raise HTTPException(status_code=404, detail="Resource not found")
        return ResponseCarDTO.model_validate(car)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Bad request")

def update_car(db: Session, car_id: int, car_data: UpdateCarDTO) -> ResponseCarDTO:
    try:
        car = db.query(Car).filter(Car.id == car_id).first()
        if not car:
            raise HTTPException(status_code=404, detail="Resource not found")

        for key, value in car_data.model_dump(exclude_unset=True).items():
            setattr(car, key, value)

        if car_data.garageIds:
            car.garages = []
            for garage_id in car_data.garageIds:
                garage = db.query(Garage).filter(Garage.id == garage_id).first()
                if garage:
                    car.garages.append(garage)
        db.commit()
        db.refresh(car)
        return ResponseCarDTO.model_validate(car)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Bad request")

def delete_car(db: Session, car_id: int) -> None:
    try:
        car = db.query(Car).filter(Car.id == car_id).first()
        if not car:
            raise HTTPException(status_code=404, detail="Resource not found")
        db.delete(car)
        db.commit()
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Bad request")

def get_all_cars(db: Session,carMake: Optional[str] = None, garageId: Optional[int] = None,fromYear: Optional[int] = None, toYear: Optional[int] = None) -> list[ResponseCarDTO]:
    try:
        query = db.query(Car)

        if carMake:
            query = query.filter(Car.make.ilike(f"%{carMake}%"))

        if garageId is not None:
            query = query.join(Car.garages).filter(Garage.id == garageId)

        if fromYear is not None:
            query = query.filter(Car.productionYear >= fromYear)

        if toYear is not None:
            query = query.filter(Car.productionYear <= toYear)

        print(str(query))

        cars = query.all()

        return [ResponseCarDTO.model_validate(car) for car in cars]
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Bad request")

