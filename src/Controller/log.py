from loguru import logger
from datetime import datetime
import os

class Logger:
    def __init__(self, log_dir):
        self.log_dir = log_dir
        self.log_file = self.generate_log_file()
        self.configure_logger()
    
    def generate_log_file(self):
        now = datetime.now()
        formatted_datetime = now.strftime("%Y-%m-%d_%H-%M-%S")
        log_file = os.path.join(self.log_dir, f"Report_{formatted_datetime}.log")
        return log_file
    
    def configure_logger(self):
        logger.remove()  # 기존 핸들러 제거
        logger.add(self.log_file, level="DEBUG", format="<green>{time:YYYY-MM-DD HH:mm:ss.SS}</green> | <level>{level: <8}</level> | <level>{message}</level>", rotation="1 week", retention="2 weeks")
    
    def get_logger(self):
        return logger

if __name__ == "__main__":
    log_dir = "src\\log"  # 로그 파일의 디렉토리 경로
    logger_instance = Logger(log_dir)
    logger = logger_instance.get_logger()
    
    # Example usage
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
