from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database.database import Base

class Garage(Base):
    __tablename__ = "garages"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    city = Column(String)
    capacity = Column(Integer)
    cars = relationship("Car", back_populates="garages")
    maintenances = relationship("Maintenance", back_populates="garage")

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    make = Column(String)
    model = Column(String)
    productionYear = Column(Integer)
    licensePlate = Column(String)
    garage_id = Column(Integer, ForeignKey('garages.id'))
    garages = relationship("Garage", secondary="car_garage", back_populates="cars")
    maintenances = relationship("Maintenance", back_populates="car")

class CarGarage(Base):
    __tablename__ = "car_garage"

    car_id = Column(Integer, ForeignKey('cars.id'), primary_key=True)
    garage_id = Column(Integer, ForeignKey('garages.id'), primary_key=True)

class Maintenance(Base):
    __tablename__ = "maintenances"

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id"))
    serviceType = Column(String)
    garage_id = Column(Integer, ForeignKey("garages.id"))
    scheduledDate = Column(Date)
    car = relationship("Car", back_populates="maintenances")
    garage = relationship("Garage", back_populates="maintenances")