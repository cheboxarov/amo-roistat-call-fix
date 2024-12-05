from loguru import logger
from telegram_logging.services import create_telegram_logger_from_dotenv
from threading import Thread

def configure_loguru():
    logger.add("logs/debug.log", level="DEBUG")
    telegram_logger = create_telegram_logger_from_dotenv()
    if telegram_logger:
        def logger_handler(message: str):
            Thread(target=telegram_logger.send_log, args=(message,), daemon=True).start()
        logger.add(logger_handler, level="ERROR")