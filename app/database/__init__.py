from app.database.base import Base, engine, get_db

# 导入所有模型，确保它们被注册到Base.metadata中
from app.models import User


def init_db():
    """初始化数据库，创建所有表"""
    Base.metadata.create_all(bind=engine)
