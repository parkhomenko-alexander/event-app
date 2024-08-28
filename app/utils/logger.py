import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from settings import config


def setup_logging(logger_path, logger_filename):
    logger = logging.getLogger("events_application_sitcenter")
    
    logger.setLevel(logging.INFO)
    if not logger.hasHandlers(): 
        root_dir = sys.path[1]
        log_file_path = os.path.join(root_dir, logger_path, logger_filename)
        
        console_handler = logging.StreamHandler()
        file_handler = RotatingFileHandler(log_file_path, maxBytes=200000, backupCount=10)
        
        console_handler.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        
        format = "[%(asctime)s] %(module)s:%(lineno)d :: %(levelname)-7s :: %(message)s"
        console_format = logging.Formatter(format)
        file_format = logging.Formatter(format)
        
        console_handler.setFormatter(console_format)
        file_handler.setFormatter(file_format)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.propagate = False

    return logger

log = setup_logging(config.APPLICATION_LOGGER_PATH, config.APPLICATION_LOGGER_FILENAME)