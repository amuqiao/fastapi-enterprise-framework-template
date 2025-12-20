from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.base import get_db
from app.middleware.authentication import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """获取当前用户信息"""
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """根据ID获取用户信息"""
    # 这里可以添加权限检查，比如只有管理员可以查看其他用户信息
    from app.services.user_service import UserService
    return UserService.get_user_by_id(db, user_id)
