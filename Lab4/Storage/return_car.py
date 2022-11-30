from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class ReturnCar(Base):
    __tablename__ = 'return_car'

    id = Column(Integer, primary_key = True )
    traceId = Column(String(250), nullable=False)
    carId = Column(String, nullable=False )
    kilometers = Column(Integer, nullable=False)
    gasUsed = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)
    rentDuration = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, carId, kilometers, gasUsed, cost, rentDuration, traceId):
        """ Initializes a rented car """
        self.carId = carId
        self.traceId = traceId
        self.kilometers = kilometers
        self.gasUsed = gasUsed
        self.date_created = datetime.datetime.now() # Sets the date/time record is created
        self.cost = cost
        self.rentDuration = rentDuration

    def to_dict(self):
        """ Dictionary Representation of a blood pressure reading """
        dict = {}
        dict['carId'] = self.carId
        dict['traceId'] = self.traceId
        dict['kilometers'] = self.kilometers
        dict['gasUsed'] = self.gasUsed
        dict['cost'] = self.cost
        dict['rentDuration'] = self.rentDuration
        dict['date_created'] = self.date_created

        return dict