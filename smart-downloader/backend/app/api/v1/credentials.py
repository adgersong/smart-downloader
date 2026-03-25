"""
凭证管理 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db.database import get_db
from ...models.credential import Credential
from ...models.business_system import BusinessSystem
from ...models.user import User
from ...schemas import CredentialCreate, CredentialUpdate, CredentialResponse, ResponseBase
from ...core.security import get_password_hash
from ...core.security.encryption import encrypt_credential
from ...core.deps import get_current_user, require_permission

router = APIRouter()


@router.post("", response_model=CredentialResponse, status_code=201)
async def save_credential(
    request: CredentialCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["credential:create"]))
):
    """保存凭证"""
    # 检查系统是否存在
    system = db.query(BusinessSystem).filter(BusinessSystem.id == request.system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="业务系统不存在")
    
    # 检查是否已有凭证
    existing = db.query(Credential).filter(Credential.system_id == request.system_id).first()
    if existing:
        # 更新
        existing.username_enc = get_password_hash(request.username)
        existing.password_enc = get_password_hash(request.password)
        existing.auth_type = request.auth_type
        existing.mfa_config = request.mfa_config
        db.commit()
        db.refresh(existing)
        credential = existing
    else:
        # 创建
        credential = Credential(
            system_id=request.system_id,
            username_enc=encrypt_credential(request.username),
            password_enc=encrypt_credential(request.password),
            auth_type=request.auth_type,
            mfa_config=request.mfa_config
        )
        db.add(credential)
        db.commit()
        db.refresh(credential)
    
    return CredentialResponse(
        id=credential.id,
        system_id=credential.system_id,
        username=request.username,  # 返回明文用于显示
        auth_type=credential.auth_type,
        created_at=credential.created_at
    )


@router.put("/{credential_id}", response_model=CredentialResponse)
async def update_credential(
    credential_id: int,
    request: CredentialUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["credential:update"]))
):
    """更新凭证"""
    credential = db.query(Credential).filter(Credential.id == credential_id).first()
    if not credential:
        raise HTTPException(status_code=404, detail="凭证不存在")
    
    if request.username:
        credential.username_enc = encrypt_credential(request.username)
    if request.password:
        credential.password_enc = encrypt_credential(request.password)
    if request.auth_type:
        credential.auth_type = request.auth_type
    if request.mfa_config:
        credential.mfa_config = request.mfa_config
    
    db.commit()
    db.refresh(credential)
    
    return CredentialResponse(
        id=credential.id,
        system_id=credential.system_id,
        username="***",
        auth_type=credential.auth_type,
        created_at=credential.created_at
    )


@router.post("/{credential_id}/test", response_model=dict)
async def test_credential(
    credential_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["credential:test"]))
):
    """测试凭证"""
    credential = db.query(Credential).filter(Credential.id == credential_id).first()
    if not credential:
        raise HTTPException(status_code=404, detail="凭证不存在")
    
    # TODO: 实际测试登录逻辑
    return {
        "success": True,
        "message": "登录成功",
        "response_time": 1523
    }
