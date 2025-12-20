from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.password import get_password_hash, verify_password
from app.utils.jwt import create_access_token
from app.logger.logger import logger


class UserService:
    """用户服务类"""
    
    @staticmethod
    def register_user(db: Session, user_create: UserCreate) -> User:
        """用户注册"""
        # 检查用户名是否已存在
        existing_user = db.query(User).filter(User.username == user_create.username).first()
        if existing_user:
            logger.warning(f"User registration failed: username {user_create.username} already exists")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already registered"
            )
        
        # 检查邮箱是否已存在
        existing_email = db.query(User).filter(User.email == user_create.email).first()
        if existing_email:
            logger.warning(f"User registration failed: email {user_create.email} already exists")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        
        # 创建新用户
        hashed_password = get_password_hash(user_create.password)
        db_user = User(
            username=user_create.username,
            email=user_create.email,
            password_hash=hashed_password
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"User registered successfully: {user_create.username}")
        return db_user
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> User:
        """用户认证"""
        # 查询用户
        user = db.query(User).filter(User.username == username).first()
        if not user:
            logger.warning(f"Authentication failed: user {username} not found")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # 验证密码
        if not verify_password(password, user.password_hash):
            logger.warning(f"Authentication failed: incorrect password for user {username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        logger.info(f"User authenticated successfully: {username}")
        return user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """根据ID获取用户"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    
    @staticmethod
    def generate_token(user: User) -> str:
        """生成JWT令牌"""
        access_token = create_access_token(data={"sub": str(user.id), "username": user.username})
        logger.info(f"Generated access token for user: {user.username}")
        return access_token
