"""
权限管理 API 路由（RBAC）
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ...db.database import get_db
from ...models.permission import Permission
from ...models.user import User
from ...schemas import (
    PermissionCreate,
    PermissionUpdate,
    PermissionResponse,
    PaginatedResponse,
    ResponseBase,
)
from ...core.deps import get_current_user, require_permission

router = APIRouter()

# -------------------- 权限列表（分页） --------------------
@router.get("", response_model=PaginatedResponse)
async def list_permissions(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    # 仅管理员可以查看全部权限
    _: None = Depends(require_permission(["admin:manage_permissions"]))
):
    query = db.query(Permission)
    total = query.count()
    items = (
        query.order_by(Permission.id.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    return PaginatedResponse(
        data={
            "items": [PermissionResponse.from_orm(item) for item in items],
            "pagination": {
                "page": page,
                "size": size,
                "total": total,
                "total_pages": (total + size - 1) // size,
            },
        }
    )



# -------------------- 创建权限 --------------------
@router.post("", response_model=PermissionResponse)
async def create_permission(
    payload: PermissionCreate,
    db: Session = Depends(get_db),
    _: None = Depends(require_permission(["admin:manage_permissions"]))
):
    # 检查重复
    exists = db.query(Permission).filter(Permission.name == payload.name).first()
    if exists:
        raise HTTPException(status_code=400, detail="权限已存在")
    perm = Permission(name=payload.name, description=payload.description)
    db.add(perm)
    db.commit()
    db.refresh(perm)
    return PermissionResponse.from_orm(perm)

# -------------------- 获取单个权限 --------------------
@router.get("/{perm_id}", response_model=PermissionResponse)
async def get_permission(
    perm_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_permission(["admin:manage_permissions"]))
):
    perm = db.query(Permission).filter(Permission.id == perm_id).first()
    if not perm:
        raise HTTPException(status_code=404, detail="权限不存在")
    return PermissionResponse.from_orm(perm)

# -------------------- 更新权限 --------------------
@router.put("/{perm_id}", response_model=PermissionResponse)
async def update_permission(
    perm_id: int,
    payload: PermissionUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(require_permission(["admin:manage_permissions"]))
):
    perm = db.query(Permission).filter(Permission.id == perm_id).first()
    if not perm:
        raise HTTPException(status_code=404, detail="权限不存在")
    if payload.name is not None:
        perm.name = payload.name
    if payload.description is not None:
        perm.description = payload.description
    db.commit()
    db.refresh(perm)
    return PermissionResponse.from_orm(perm)

# -------------------- 删除权限 --------------------
@router.delete("/{perm_id}", response_model=ResponseBase)
async def delete_permission(
    perm_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_permission(["admin:manage_permissions"]))
):
    perm = db.query(Permission).filter(Permission.id == perm_id).first()
    if not perm:
        raise HTTPException(status_code=404, detail="权限不存在")
    db.delete(perm)
    db.commit()
    return ResponseBase(data={"deleted_id": perm_id})
