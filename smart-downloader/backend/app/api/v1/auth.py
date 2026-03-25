"""
认证 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ...db.database import get_db
from ...models.user import User
from ...models.organization import Organization
from ...schemas import LoginRequest, LoginResponse, UserInfo, TokenResponse, ResponseBase
from ...core.security import create_access_token, get_password_hash
from ...core.deps import get_current_user, security
import hashlib

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """用户登录"""
    # 验证组织
    org = db.query(Organization).filter(Organization.id == request.org_id).first()
    if not org:
        raise HTTPException(status_code=400, detail="组织不存在")
    
    # 验证用户
    user = db.query(User).filter(
        User.username == request.username,
        User.org_id == request.org_id
    ).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="用户已禁用")
    
    # 验证密码 (支持 bcrypt 和 sha256)
    password_hash = hashlib.sha256(request.password.encode()).hexdigest()
    if user.password_hash != password_hash:
        # 尝试 bcrypt 验证
        try:
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"])
            if not pwd_context.verify(request.password, user.password_hash):
                raise HTTPException(status_code=401, detail="密码错误")
        except:
            raise HTTPException(status_code=401, detail="密码错误")
    
    # 更新最后登录时间
    user.last_login = datetime.utcnow()
    db.commit()
    
    # 生成 Token
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=1440)
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="Bearer",
        expires_in=86400,
        user=UserInfo(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            org_id=user.org_id,
            org_name=org.name
        )
    )


@router.post("/logout", response_model=ResponseBase)
async def logout(current_user: User = Depends(get_current_user)):
    """用户登出"""
    # 在实际实现中可以将 token 加入黑名单或在前端删除
    return ResponseBase()


@router.post("/refresh-token", response_model=TokenResponse)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """刷新 Access Token"""
    from ...core.config.settings import Settings
    from ...core.security import create_access_token, decode_access_token
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="无效的 Token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token 缺失用户信息")
    # 生成新 token，使用设置的过期时间
    settings = Settings()
    new_token = create_access_token({"sub": str(user_id)}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return TokenResponse(access_token=new_token, token_type="Bearer", expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)



@router.get("/me", response_model=UserInfo)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return UserInfo(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        role=current_user.role,
        org_id=current_user.org_id,
        org_name=current_user.organization.name
    )
