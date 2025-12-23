import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 创建测试数据库引擎
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 创建测试会话工厂
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """创建测试数据库会话"""
    # 只导入DDD相关组件
    from app.domains.base.models.base import Base
    from app.domains.user.models.user import User

    # 创建所有表
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # 测试结束后删除所有表
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_user(db):
    """创建测试用户"""
    from app.domains.user.models.user import User
    from app.utils.password import get_password_hash

    # 创建测试用户
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=get_password_hash("testpassword"),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
