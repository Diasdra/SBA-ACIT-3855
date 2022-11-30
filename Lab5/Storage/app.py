import connexion
from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from rent_car import RentCar
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

def rent_car(body):
    """ Receives a car rental application """

    session = DB_SESSION()

    car_rent = RentCar(body['car_id'],
                       body['car_type'],
                       body['location'],
                       body['mileage'],
                       body['passenger_limit'],
                       body['trace_id'])

    session.add(car_rent)
    session.commit()
    session.close()

    logger.debug(f'Stored event "rent car" request with a trace id of {body["trace_id"]}')

    return NoContent, 201


def return_car(body):
    """ Receives a car return form """

    session = DB_SESSION()

    carReturn = ReturnCar(body['car_id'],
                   body['kilometers'],
                   body['gas_used'],
                   body['cost'],
                   body['rent_duration'],
                   body['trace_id'])

    session.add(carReturn)

    session.commit()
    session.close()

    logger.debug(f'Stored event "return car" request with a trace id of {body["trace_id"]}')

    return NoContent, 201

def get_car_returns(timestamp):
    """ Gets new returns after the timestamp """
    session = DB_SESSION()

    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

    readings = session.query(ReturnCar).filter(ReturnCar.date_created >=timestamp_datetime)

    results_list = []

    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()

    logger.info("Query for Car Returns readings after %s returns %d results" %(timestamp, len(results_list)))

    return results_list, 200

def get_car_rentals(timestamp):
    """ Gets new rentals after the timestamp """
    session = DB_SESSION()

    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

    readings = session.query(RentCar).filter(RentCar.date_created >=timestamp_datetime)

    results_list = []

    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()

    logger.info("Query for Car Rentals readings after %s returns %d results" %(timestamp, len(results_list)))

    return results_list, 200



app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

logger = logging.getLogger('basicLogger')
logger.debug("debug message")


if __name__ == "__main__":
    app.run(port=8090)
