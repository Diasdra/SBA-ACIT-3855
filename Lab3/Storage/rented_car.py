from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class RentedCar(Base):
    __tablename__ = 'rented_car'

    id = Column(Integer, primary_key = True )
    carId = Column(String(250), primary_key = True )
    location = Column(String(250), nullable=False)
    mileage = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)
    passengerLimit = Column(Integer, nullable=False)
    returnDate = Column(String(100), nullable=False)

    def __init__(self, carId, location, mileage, passengerLimit, returnDate):
        """ Initializes a rented car """
        self.carId = carId
        self.location = location
        self.mileage = mileage
        self.date_created = datetime.datetime.now() # Sets the date/time record is created
        self.passengerLimit = passengerLimit
        self.returnDate = returnDate

    def to_dict(self):
        """ Dictionary Representation of a blood pressure reading """
        dict = {}
        dict['carId'] = self.carId
        dict['location'] = self.location
        dict['mileage'] = self.mileage
        dict['passengerLimit'] = self.passengerLimit
        dict['returnDate'] = self.returnDate
        dict['date_created'] = self.date_created

        return dict
