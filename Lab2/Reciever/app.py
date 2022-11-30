import datetime
import json
import swagger_ui_bundle
import connexion
import os
from connexion import NoContent

data = []

def doDataThings(body):
    #insert data into array, once length is 10, print the data to a file
    #e.g events.json
    # Create a datetime object with the current date and time
    current_datetime = datetime.datetime.now()
    # Create a string with the datetime in the given format
    current_datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    body['datetime'] = current_datetime_str
    endData = logData(body)
    logJson(endData)


def logJson(content):
    with open('events.json', 'w') as logfile:
        json.dump(content, logfile, indent=4)

def logData(content):
    data.insert(0,content)
    if len(data) > 10:
        data.pop()
    return data

def returnCar(body):
    """returns a rented car back to the store"""   
    doDataThings(body)
    return NoContent, 201

def rentCar(body):
    """rents a car from the store"""
    doDataThings(body)
    return NoContent, 201

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)


if __name__ == "__main__":
    app.run(port=8080)
