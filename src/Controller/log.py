import logging
from logging.handlers import FileHandler
import datetime

class CustomFileHandler(FileHandler):
    def __init__(self, filename_prefix, filename_suffix, *args, **kwargs):
        now = datetime.datetime.now()
        formatted_datetime = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{filename_prefix}_{formatted_datetime}{filename_suffix}"
        super(CustomFileHandler, self).__init__(filename, *args, **kwargs)

class Logger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.formatter = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.stream_handler = logging.StreamHandler()
        self.file_handler = CustomFileHandler("Report", ".log")
        
        self.stream_handler.setFormatter(self.formatter)
        self.file_handler.setFormatter(self.formatter)
        
        self.logger.addHandler(self.stream_handler)
        self.logger.addHandler(self.file_handler)
        self.logger.setLevel(level=logging.DEBUG)
    
    def get_logger(self):
        return self.logger

if __name__ == "__main__":
    logger_instance = Logger()
    logger = logger_instance.get_logger()
    
    # Example usage
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
