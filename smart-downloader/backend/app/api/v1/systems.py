"""
业务系统 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from ...db.database import get_db
from ...models.business_system import BusinessSystem
from ...models.user import User
from ...schemas import BusinessSystemCreate, BusinessSystemUpdate, BusinessSystemResponse, PaginatedResponse, ResponseBase
from ...core.deps import get_current_user, require_permission

router = APIRouter()


@router.get("", response_model=PaginatedResponse)
async def get_systems(
    org_id: int = Query(...),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["system:read"]))
):
    """获取业务系统列表"""
    query = db.query(BusinessSystem).filter(BusinessSystem.org_id == org_id)
    
    if type:
        query = query.filter(BusinessSystem.type == type)
    
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    
    return PaginatedResponse(
        data={
            "items": [
                BusinessSystemResponse(
                    id=item.id,
                    org_id=item.org_id,
                    name=item.name,
                    url=item.url,
                    type=item.type,
                    description=item.description,
                    login_config=item.login_config,
                    has_credential=item.credential is not None,
                    workflow_count=len(item.workflows),
                    created_at=item.created_at,
                    updated_at=item.updated_at
                ) for item in items
            ],
            "pagination": {
                "page": page,
                "size": size,
                "total": total,
                "total_pages": (total + size - 1) // size
            }
        }
    )


@router.get("/{system_id}", response_model=BusinessSystemResponse)
async def get_system(
    system_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["system:read"]))
):
    """获取业务系统详情"""
    system = db.query(BusinessSystem).filter(BusinessSystem.id == system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="业务系统不存在")
    
    return BusinessSystemResponse(
        id=system.id,
        org_id=system.org_id,
        name=system.name,
        url=system.url,
        type=system.type,
        description=system.description,
        login_config=system.login_config,
        has_credential=system.credential is not None,
        workflow_count=len(system.workflows),
        created_at=system.created_at,
        updated_at=system.updated_at
    )


@router.post("", response_model=BusinessSystemResponse, status_code=201)
async def create_system(
    request: BusinessSystemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["system:create"]))
):
    """创建业务系统"""
    system = BusinessSystem(
        org_id=request.org_id,
        name=request.name,
        url=request.url,
        type=request.type,
        description=request.description,
        login_config=request.login_config
    )
    db.add(system)
    db.commit()
    db.refresh(system)
    
    return BusinessSystemResponse(
        id=system.id,
        org_id=system.org_id,
        name=system.name,
        url=system.url,
        type=system.type,
        description=system.description,
        login_config=system.login_config,
        created_at=system.created_at,
        updated_at=system.updated_at
    )


@router.put("/{system_id}", response_model=BusinessSystemResponse)
async def update_system(
    system_id: int,
    request: BusinessSystemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["system:update"]))
):
    """更新业务系统"""
    system = db.query(BusinessSystem).filter(BusinessSystem.id == system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="业务系统不存在")
    
    if request.name:
        system.name = request.name
    if request.url:
        system.url = request.url
    if request.type:
        system.type = request.type
    if request.description is not None:
        system.description = request.description
    if request.login_config:
        system.login_config = request.login_config
    
    db.commit()
    db.refresh(system)
    
    return BusinessSystemResponse(
        id=system.id,
        org_id=system.org_id,
        name=system.name,
        url=system.url,
        type=system.type,
        description=system.description,
        login_config=system.login_config,
        created_at=system.created_at,
        updated_at=system.updated_at
    )


@router.delete("/{system_id}", response_model=ResponseBase)
async def delete_system(
    system_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["system:delete"]))
):
    """删除业务系统"""
    system = db.query(BusinessSystem).filter(BusinessSystem.id == system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="业务系统不存在")
    
    db.delete(system)
    db.commit()
    
    return ResponseBase()
