from fastapi import Depends
from app.databases.base import database_manager
from app.databases.sqlite.connection import sqlite_connection

# 注册数据库连接
database_manager.register("sqlite", sqlite_connection)

# 导出数据库连接实例
sqlite = sqlite_connection


# 依赖注入函数 - 用于FastAPI Depends
def get_sqlite_db():
    """SQLite数据库会话依赖注入"""
    yield from sqlite_connection.get_session()


# 依赖注入容器 - 用于FastAPI Depends
class DatabaseDeps:
    """数据库依赖注入容器，提供统一的依赖注入接口"""

    @staticmethod
    def sqlite():
        return Depends(get_sqlite_db)


# 导出依赖注入容器
deps = DatabaseDeps()
