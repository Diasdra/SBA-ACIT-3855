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

client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
topic = client.topics[str.encode(app_config['events']['topic'])]
producer = topic.get_sync_producer()

def return_car(body):
    trace = str(uuid.uuid4())
    body['trace_id'] = trace

    logger.info('Received return car event with trace id' + trace)

    #res = requests.post(app_config['return_car']['url'], headers={'Content-Type' : 'application/json'}, json=body)
    msg = { "type": "return_car", "datetime" :datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
            
    #logger.info('Returned return car event response(Id: ' + trace + ') with status' + str(res.status_code))

    return body, 201

def rent_car(body):
    trace = str(uuid.uuid4())
    body['trace_id'] = trace

    logger.info('Received rentcar even with trace id' + trace)

    #res = requests.post(app_config['rent_car']['url'], headers={'Content-Type' : 'application/json'}, data=json.dumps(body))
    msg = { "type": "rent_car", "datetime" :datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    #logger.info('Returned rent car event response(Id: ' + trace + ') with status' + str(res.status_code))

    return body, 201

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

logger = logging.getLogger('basicLogger')
logger.debug("debug message")

if __name__ == "__main__":
    app.run(port=8080)
