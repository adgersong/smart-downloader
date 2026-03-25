"""
组织管理 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from ...db.database import get_db
from ...models.organization import Organization
from ...models.user import User
from ...schemas import (
    OrganizationCreate, OrganizationUpdate, OrganizationResponse,
    OrganizationStats, PaginatedResponse, ResponseBase
)
from ...core.deps import get_current_user, require_permission, require_permission

router = APIRouter()


@router.get("", response_model=PaginatedResponse)
async def get_organizations(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["org:read"]))
):
    """获取组织列表"""
    query = db.query(Organization)
    
    if keyword:
        query = query.filter(Organization.name.contains(keyword))
    
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    
    return PaginatedResponse(
        data={
            "items": [
                OrganizationResponse(
                    id=item.id,
                    name=item.name,
                    config=item.config,
                    stats=OrganizationStats(
                        user_count=len(item.users),
                        system_count=len(item.systems),
                        workflow_count=len(item.workflows),
                        task_count=sum(len(wf.tasks) for wf in item.workflows)
                    ),
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


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(
    org_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["org:read"]))
):
    """获取组织详情"""
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="组织不存在")
    
    return OrganizationResponse(
        id=org.id,
        name=org.name,
        config=org.config,
        stats=OrganizationStats(
            user_count=len(org.users),
            system_count=len(org.systems),
            workflow_count=len(org.workflows),
            task_count=sum(len(wf.tasks) for wf in org.workflows)
        ),
        created_at=org.created_at,
        updated_at=org.updated_at
    )


@router.post("", response_model=OrganizationResponse, status_code=201)
async def create_organization(
    request: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["org:create"]))
):
    """创建组织"""
    # 检查名称是否重复
    existing = db.query(Organization).filter(Organization.name == request.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="组织名称已存在")
    
    org = Organization(
        name=request.name,
        config=request.config or {}
    )
    db.add(org)
    db.commit()
    db.refresh(org)
    
    return OrganizationResponse(
        id=org.id,
        name=org.name,
        config=org.config,
        created_at=org.created_at,
        updated_at=org.updated_at
    )


@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: int,
    request: OrganizationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["org:update"]))
):
    """更新组织"""
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="组织不存在")
    
    # 检查名称是否重复
    if request.name and request.name != org.name:
        existing = db.query(Organization).filter(
            Organization.name == request.name,
            Organization.id != org_id
        ).first()
        if existing:
            raise HTTPException(status_code=409, detail="组织名称已存在")
        org.name = request.name
    
    if request.config:
        org.config = request.config
    
    db.commit()
    db.refresh(org)
    
    return OrganizationResponse(
        id=org.id,
        name=org.name,
        config=org.config,
        created_at=org.created_at,
        updated_at=org.updated_at
    )


@router.delete("/{org_id}", response_model=ResponseBase)
async def delete_organization(
    org_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["org:delete"]))
):
    """删除组织"""
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="组织不存在")
    
    db.delete(org)
    db.commit()
    
    return ResponseBase()
