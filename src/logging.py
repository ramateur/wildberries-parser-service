import logging
from logging.handlers import TimedRotatingFileHandler
import os

from src.config import settings


logging_level = logging.DEBUG if settings.DEBUG else logging.INFO

logs_format = '%(asctime)s - %(processName)s - %(module)s - %(levelname)s - %(message)s'

# Configure root logger
logging.basicConfig(level=logging_level, format=logs_format)


def setup_file_logger(
    logs_folder: str = 'logs',
    logs_subfolder: str | None = None,
    logs_file_name: str = 'parser.log',
    log_format: str = logs_format,
    rotate_when: str = 'midnight',
    rotate_interval: int = 1,
    rotate_backup_count=7,
):
    # Specify the 'logs' folder
    logs_path = logs_folder + '/' + logs_subfolder if logs_subfolder else logs_folder
    os.makedirs(logs_path, exist_ok=True)
    logs_file_name = 'debug.' + logs_file_name if settings.DEBUG else logs_file_name
    log_file_path = os.path.join(logs_path, logs_file_name)

    # Configure TimedRotatingFileHandler for rotating logs
    file_handler = TimedRotatingFileHandler(
        log_file_path, when=rotate_when, interval=rotate_interval, backupCount=rotate_backup_count
    )
    file_handler.setLevel(logging_level)
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)

    # Add the handler to the root logger
    logging.getLogger('').addHandler(file_handler)

    # Set logging level for specific loggers
    loggers = ['sentence_transformers', 'elasticsearch', 'httpx']
    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO if settings.DEBUG else logging.ERROR)
