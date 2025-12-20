from app.config.base import BaseSettings
from typing import Optional, Dict, Any


class LoggingConfig(BaseSettings):
    """日志配置"""

    # 日志级别配置
    LEVEL: str = "INFO"  # 主日志级别：DEBUG, INFO, WARNING, ERROR, CRITICAL

    # 日志文件配置
    FILE: Optional[str] = "logs/app.log"  # 日志文件路径，None表示不输出到文件
    MAX_BYTES: int = 10 * 1024 * 1024  # 单个日志文件最大字节数(10MB)
    BACKUP_COUNT: int = 5  # 保留的日志文件数量

    # 日志格式配置
    FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    # 控制台日志配置
    CONSOLE_LEVEL: Optional[str] = None  # 控制台日志级别，None表示与主级别相同

    # 文件日志配置
    FILE_LEVEL: Optional[str] = None  # 文件日志级别，None表示与主级别相同

    # 日志模块级别配置 - 可以为不同模块设置不同日志级别
    MODULE_LEVELS: Dict[str, str] = {
        "uvicorn": "INFO",
        "fastapi": "INFO",
        "sqlalchemy": "WARNING",
        "app": "INFO",
    }

    # 是否禁用默认日志配置
    DISABLE_DEFAULT_LOGGERS: bool = False

    model_config = BaseSettings.model_config.copy()
    model_config["env_prefix"] = "LOGGING_"


# 创建日志配置实例
logging_config = LoggingConfig()
