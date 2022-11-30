import connexion
from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from rented_car import RentedCar
from return_car import ReturnCar
import datetime

DB_ENGINE = create_engine("sqlite:///CarRenting.sqlite")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def rentCar(body):
    """ Receives a car rental application """

    session = DB_SESSION()

    carRent = RentedCar(body['carId'],
                       body['location'],
                       body['mileage'],
                       body['passengerLimit'],
                       body['returnDate'])

    session.add(carRent)

    session.commit()
    session.close()

    return NoContent, 201


def returnCar(body):
    """ Receives a heart rate (pulse) reading """

    session = DB_SESSION()

    carReturn = ReturnCar(body['carId'],
                   body['kilometers'],
                   body['gasUsed'],
                   body['cost'],
                   body['rentDuration'])

    session.add(carReturn)

    session.commit()
    session.close()

    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8090)
