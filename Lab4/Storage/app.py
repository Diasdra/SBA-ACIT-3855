import connexion
from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from rented_car import RentedCar
from return_car import ReturnCar
import datetime
import logging
import uuid
from logging import config
import requests
import yaml


with open('app_conf.yml', 'r') as f:
  db_config = yaml.safe_load(f.read())
  db_config = db_config['datastore']

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)


DB_ENGINE = create_engine(f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['hostname']}:{db_config['port']}/{db_config['db']}")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def rentCar(body):
    """ Receives a car rental application """

    session = DB_SESSION()

    carRent = RentedCar(body['carId'],
                       body['location'],
                       body['mileage'],
                       body['passengerLimit'],
                       body['returnDate'],
                       body['traceId'])

    session.add(carRent)
    session.commit()
    session.close()

    logger.debug(f'Stored event "rent car" request with a trace id of {body["traceId"]}')

    return NoContent, 201


def returnCar(body):
    """ Receives a heart rate (pulse) reading """

    session = DB_SESSION()

    carReturn = ReturnCar(body['carId'],
                   body['kilometers'],
                   body['gasUsed'],
                   body['cost'],
                   body['rentDuration'],
                   body['traceId'])

    session.add(carReturn)

    session.commit()
    session.close()

    logger.debug(f'Stored event "return car" request with a trace id of {body["traceId"]}')

    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

logger = logging.getLogger('basicLogger')
logger.debug("debug message")


if __name__ == "__main__":
    app.run(port=8090)
