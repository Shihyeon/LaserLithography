from loguru import logger
from datetime import datetime
import os

class Logger:
    def __init__(self, log_dir="src\\log"):
        self.log_dir = log_dir
        self.log_file = self.generateLogFile()
        self.configureLogger()
    
    def generateLogFile(self):
        now = datetime.now()
        formatted_datetime = now.strftime("%Y-%m-%d_%H-%M-%S")
        log_file = os.path.join(self.log_dir, f"Report_{formatted_datetime}.log")
        return log_file
    
    def configureLogger(self):
        logger.remove()  # 기존 핸들러 제거
        logger.add(self.log_file, level="TRACE", format="<green>{time:YYYY-MM-DD HH:mm:ss.SS}</green> | <level>{level: <8}</level> | <level>{message}</level>", rotation="1 week", retention="2 weeks")
    
    def getLogger(self):
        return logger

if __name__ == "__main__":
    log_dir = "src\\log"  # 로그 파일의 디렉토리 경로
    logger_instance = Logger(log_dir)
    logger = logger_instance.getLogger()
    
    # Example usage
    logger.trace("This is a trace message")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.success("This is a success message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
