import datetime
import json
import swagger_ui_bundle
import connexion
import os
import yaml
import logging
import uuid
from logging import config
from connexion import NoContent
from pykafka import KafkaClient
import requests

with open('app_conf.yml', 'r') as f:
  app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

def get_return_car_application(index):
    """ Get return car app in History """
    
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    
    # Here we reset the offset on start so that we retrieve
    # messages at the beginning of the message queue.
    # To prevent the for loop from blocking, we set the timeout to
    # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received!
    
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
    
    logger.info("Retrieving return car at index %d" % index)
    try:
        pos = 0
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            logger.info(msg)
            if  msg["type"] == "return_car":
                if index == pos:
                    logger.info(f'found return_car application at index {index}: {msg}')
                    return msg, 200
                pos+=1

        logger.error("Could not find return car at index %d" % index)
    except:
        logger.error("No more messages found")
        logger.error("Could not find return car at index %d" % index)
        return { "message": "Not Found"}, 404

def get_rent_car_application(index):
    """ Get rent car app in History """
    
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    
    # Here we reset the offset on start so that we retrieve
    # messages at the beginning of the message queue.
    # To prevent the for loop from blocking, we set the timeout to
    # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received!
    
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
    
    logger.info("Retrieving rent car at index %d" % index)
    try:
        pos = 0
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            logger.info(msg)
            if  msg["type"] == "rent_car":
                if index == pos:
                    logger.info(f'found rent_car application at index {index}: {msg}')
                    return msg, 200
                pos+=1
        logger.error("Could not find rent car at index %d" % index)
    except:
        logger.error("No more messages found")
        logger.error("Could not find rent car at index %d" % index)
        return { "message": "Not Found"}, 404

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

logger = logging.getLogger('basicLogger')
logger.debug("debug message")

if __name__ == "__main__":
    app.run(port=8110)
