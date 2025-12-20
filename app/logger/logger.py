import logging
import os
from logging.handlers import RotatingFileHandler
from logging.config import dictConfig
from app.config import logging_config


def setup_logging():
    """配置日志系统"""
    # 创建日志目录
    if logging_config.FILE:
        log_dir = os.path.dirname(logging_config.FILE)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    # 构建日志配置字典
    log_config = {
        "version": 1,
        "disable_existing_loggers": logging_config.DISABLE_DEFAULT_LOGGERS,
        "formatters": {
            "standard": {
                "format": logging_config.FORMAT,
                "datefmt": logging_config.DATE_FORMAT
            },
        },
        "handlers": {
            "console": {
                "level": logging_config.CONSOLE_LEVEL or logging_config.LEVEL,
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "app": {
                "handlers": ["console"],
                "level": logging_config.LEVEL,
                "propagate": False
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "WARNING",
        }
    }
    
    # 添加文件处理器（如果配置了日志文件）
    if logging_config.FILE:
        log_config["handlers"]["file"] = {
            "level": logging_config.FILE_LEVEL or logging_config.LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": logging_config.FILE,
            "maxBytes": logging_config.MAX_BYTES,
            "backupCount": logging_config.BACKUP_COUNT,
            "encoding": "utf-8",
        }
        # 将文件处理器添加到app logger
        log_config["loggers"]["app"]["handlers"].append("file")
    
    # 为不同模块配置不同日志级别
    for module, level in logging_config.MODULE_LEVELS.items():
        log_config["loggers"][module] = {
            "handlers": ["console"] + (["file"] if logging_config.FILE else []),
            "level": level,
            "propagate": False
        }
    
    # 应用日志配置
    dictConfig(log_config)
    
    # 获取并返回主日志记录器
    logger = logging.getLogger("app")
    logger.info("日志系统已初始化")
    return logger


# 初始化日志系统
logger = setup_logging()
