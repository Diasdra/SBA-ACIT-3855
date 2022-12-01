import swagger_ui_bundle
import connexion
import requests
import time
import sqlalchemy
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from apscheduler.schedulers.background import BackgroundScheduler
from base import Base
from health import Health
import datetime
import logging
import uuid
from logging import config
import requests
import yaml
from flask_cors import CORS, cross_origin

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


DB_ENGINE = create_engine("sqlite:///%s" %app_config["datastore"]["filename"])
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def get_health_stats():
    """ Receives a Health req """
    
    logger.info(f"Start a health check")
    session = DB_SESSION()
    
    results = session.query(Health).order_by(Health.last_updated.desc()).first()

    if not results:
        logger.error(f'Statistics do not exist')
        return 404
    
    data = results.to_dict()
    
    logger.debug(data.items)
    logger.info("request has been completed")
    
    session.close()

    return data, 200

def check_health():
    """ Periodically update Health   """
    
    services = ['storage', 'receiver', 'processor', 'audit']
    
    now = datetime.datetime.now()

    session = DB_SESSION()
    
    results = session.query(Health).order_by(Health.last_updated.desc()).first()

    if not results:
        health = Health("Down",
                        "Down",
                        "Down",
                        "Down",
                        datetime.datetime.fromtimestamp(0))
    
    status = []
    for app in services:
        try:
            logger.info(f'Checking health of {app_config["endpoints"][app]} with timeout of {app_config["endpoints"]["timeout_time"]}')
            res = requests.get(f'{app_config["endpoints"][app]}/health')
            logger.info(f'got response of {res}')
            if res.status_code == 200:
                status.append('Running')
            else:
                status.append('Down')
        except:
            status.append('Down')
            
        
    health = Health(storage=status[0], receiver=status[1],processor=status[2],audit=status[3], last_updated=now)

    session.add(health)
    logger.debug(health)

    session.commit()
    session.close()
    
app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'

logger = logging.getLogger('basicLogger')
logger.debug("debug message")

if __name__ == "__main__":
    app.run(port=8120)
