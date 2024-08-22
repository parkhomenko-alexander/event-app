import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from settings import config


def setup_logging(logger_path, logger_filename):
    logger = logging.getLogger("events_application_sitcenter")
    
    logger.setLevel(logging.INFO)
    
    console_handler = logging.StreamHandler()
    root_dir = sys.path[1]
    file_handler = RotatingFileHandler(root_dir+logger_path+logger_filename, maxBytes=2000, backupCount=10)
    
    console_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    
    console_format = logging.Formatter("[%(asctime)s] %(module)s:%(lineno)d :: %(levelname)-7s :: %(message)s")
    file_format = logging.Formatter("[%(asctime)s] %(module)s:%(lineno)d :: %(levelname)-7s :: %(message)s")
    
    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

log = setup_logging(config.APPLICATION_LOGGER_PATH, config.APPLICATION_LOGGER_FILENAME)