from app.databases.sqlite.connection import sqlite_connection


# 导出仓储实例
def get_user_repository(db=None):
    """获取用户仓储实例"""
    from app.repositories.sqlite.user_repository import UserRepository

    return UserRepository(db)
