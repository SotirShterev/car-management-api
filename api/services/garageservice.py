from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session
from models.models import Garage
from dtos.garagedto import CreateGarageDTO,UpdateGarageDTO,ResponseGarageDTO

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

def get_all_garages(db: Session) -> list[ResponseGarageDTO]:
    try:
        garages = db.query(Garage).all()
        return [ResponseGarageDTO.model_validate(garage) for garage in garages]
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Bad request")

