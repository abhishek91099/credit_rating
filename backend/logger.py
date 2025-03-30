import logging
import os
from Config import LOG_LEVEL, LOG_FORMAT, LOG_FILE

def setup_logger(name):
    """Set up and return a logger with the given name"""
    # Convert string log level to logging constant
    log_level = getattr(logging, LOG_LEVEL.upper())
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Check if logger already has handlers to avoid duplicates
    if not logger.handlers:
        # Create formatter
        formatter = logging.Formatter(LOG_FORMAT)
        
        # Create file handler
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger