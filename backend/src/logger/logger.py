import os
import logging
from logging.handlers import RotatingFileHandler


class AppLogger:
    def __init__(
            self,
            log_file: str,
            category: str,
            level: int = logging.DEBUG
    ):
        logger_name = f"app.{category}"
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(level)

        if not self.logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
            )

            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)

            file_handler = RotatingFileHandler(
                log_file, maxBytes=1_000_000, backupCount=5
            )
            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        return self.logger
