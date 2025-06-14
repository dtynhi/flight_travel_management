import logging
import os
from datetime import datetime
from concurrent_log_handler import ConcurrentRotatingFileHandler
from config.app_config import AppConfig

_logger = logging.getLogger(__name__)


def set_up_logging(app):

    if _logger.hasHandlers():
        _logger.handlers.clear()
    _logger.setLevel(logging.DEBUG)

    log_format = logging.Formatter(
        "%(asctime)s - %(filename)s.%(funcName)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(log_format)
    _logger.addHandler(console_handler)


    if not os.path.exists(AppConfig.LOG_FILE_PATH):
        os.makedirs(AppConfig.LOG_FILE_PATH)

    log_file = os.path.join(AppConfig.LOG_FILE_PATH, f"QLMB_{datetime.now().strftime('%Y-%m-%d')}.log")

    log_handler = ConcurrentRotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding='utf-8'
    )
    log_handler.setFormatter(log_format)
    _logger.addHandler(log_handler)

    _logger.propagate = False
