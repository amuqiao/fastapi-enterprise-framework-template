import logging
import os
from logging.handlers import RotatingFileHandler
from app.core.config import settings

# 创建日志目录
log_dir = os.path.dirname(settings.LOG_FILE) if settings.LOG_FILE else None
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 配置日志格式
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 创建日志记录器
logger = logging.getLogger("app")
logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
console_handler.setFormatter(logging.Formatter(log_format))

# 添加控制台处理器到日志记录器
logger.addHandler(console_handler)

# 如果配置了日志文件，创建文件处理器
if settings.LOG_FILE:
    file_handler = RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)
