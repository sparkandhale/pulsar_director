import logging
from pathlib import Path
import yaml, sys
logger = logging.getLogger('app')

def get_project_root() -> str:    
    str_path = str(Path(__file__).parent.parent)
    #print(f"utils.py: {str_path}")
    return str_path

def get_project_root_path() -> Path:    
    abs_path = Path(__file__).parent.parent.absolute()
    return abs_path

def get_log_path() -> Path:    
    abs_path = get_project_root_path().joinpath('logs')
    return abs_path

def get_secrets_path() -> Path:    
    abs_path = get_project_root_path().joinpath('secrets')
    return abs_path

def get_app_config() -> dict:
    app_cfg = None
    with open(get_project_root_path().joinpath("config/app_config.yaml"), "r") as ymlfile:
        try:
            app_cfg = yaml.safe_load(ymlfile)   
        except yaml.YAMLError as ex:
            logger.critical(f"Failed to load the app_config.yaml file. Aborting the application. Error: {ex}")
            sys.exit(1) 
    return app_cfg

def get_application_name() -> str:
    return get_app_config()["application"]

def get_logging_level() -> str:
    return get_app_config()["logging_level"].upper()

def get_pulsar_broker_service_url() -> str:
    """Returns the pulsar broker service url."""
    return get_app_config()['pulsar_broker_service_url']

def get_cex_secrets() -> dict:
    secrets = None
    with open(get_secrets_path().joinpath("api_secrets.yaml"), "r") as ymlfile:
        try:
            secrets = yaml.safe_load(ymlfile)   
        except yaml.YAMLError as ex:
            logger.critical(f"Failed to load the api_secrets.yaml file. Aborting the application. Error: {ex}")
            sys.exit(1)
    return secrets