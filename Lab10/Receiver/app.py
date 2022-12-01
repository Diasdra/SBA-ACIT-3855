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


if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"

with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())

# External Logging Configuration
with open(log_conf_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)

kafka_max_connection_retries = app_config["kafka"]["max_retries"]
current_retry_count = 0
while current_retry_count < kafka_max_connection_retries:
    logger.info(f'Attempting to connect to kafak - Attempt #{current_retry_count}')
    try:
        client = KafkaClient(hosts=kafka_hostname)
        topic = client.topics[str.encode(kafka_topic)]
        producer = topic.get_sync_producer()
        logger.info(f'Connection Attempt #{current_retry_count} successful')
        break
    except:
        logger.error(f'Kafka connection failed. Attempt #{current_retry_count}')
        time.sleep(kafka_sleep_time_before_reconnect)
        current_retry_count += 1
        
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
