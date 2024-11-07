from loguru import logger

def configure_loguru():
    logger.add("logs/debug.log", level="DEBUG")