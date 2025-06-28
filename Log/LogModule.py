import logging
import os.path
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


class DefaultLogger:

    __instance = None
    log_dir = os.path.join(os.environ.get("PROGRAMDATA"), "SOFT", "Log_dir")

    @staticmethod
    def get_instance():
        """
        Singleton
        :return:
        """
        if DefaultLogger.__instance is None:
            DefaultLogger.__instance = DefaultLogger("SOFT.log")
        return DefaultLogger.__instance

    def __init__(self, log_file, log_level=logging.DEBUG):

        Path(self.log_dir).mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Rotating File Handler
        file_handler = TimedRotatingFileHandler(os.path.join(self.log_dir, log_file), when='midnight', interval=1, backupCount=30)
        file_handler.setFormatter(formatter)
        file_handler.namer = lambda name: name.replace(".log", "") + ".log"
        self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

# Exemple d'utilisation :
if __name__ == "__main__":
    logger = DefaultLogger("example.log")
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")