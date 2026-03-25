"""
认证依赖项
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..models.user import User
from .security import decode_access_token

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """获取当前登录用户"""
    token = credentials.credentials
    
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="认证失败",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id: int = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="认证失败",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在或已禁用",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def require_permission(required: list[str]):
    """返回一个 FastAPI 依赖函数，用于检查当前用户是否拥有指定权限"""
    async def dependency(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        from ..models.permission import Permission, role_permission
        # 直接使用用户 role（字符串）查询关联权限
        perms = (
            db.query(Permission.name)
            .join(role_permission, Permission.id == role_permission.c.permission_id)
            .filter(role_permission.c.role == current_user.role)
            .all()
        )
        user_perms = {p[0] for p in perms}
        missing = [p for p in required if p not in user_perms]
        if missing:
            raise HTTPException(
                status_code=403,
                detail=f"缺少权限: {', '.join(missing)}",
            )
        return True
    return Depends(dependency)

