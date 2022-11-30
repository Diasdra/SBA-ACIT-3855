import datetime
import json
import swagger_ui_bundle
import connexion
import os
from connexion import NoContent
import requests

RENT_URL = 'http://127.0.0.1:8090/car'
RETURN_URL = 'http://127.0.0.1:8090/return'

def returnCar(body):
    x = requests.post(RETURN_URL, json=body)
    return NoContent, x.status_code

def rentCar(body):
    x = requests.post(RENT_URL, json=body)
    return NoContent, x.status_code


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)


if __name__ == "__main__":
    app.run(port=8080)
