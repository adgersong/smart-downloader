"""
流程管理 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from ...db.database import get_db
from ...models.workflow import Workflow, WorkflowStep
from ...models.user import User
from ...schemas import WorkflowCreate, WorkflowUpdate, WorkflowResponse, WorkflowGenerateRequest, WorkflowValidationResponse, PaginatedResponse, ResponseBase
from ...core.deps import get_current_user, require_permission
import yaml

router = APIRouter()


@router.get("", response_model=PaginatedResponse)
async def get_workflows(
    org_id: int = Query(...),
    system_id: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["workflow:read"]))
):
    """获取流程列表"""
    query = db.query(Workflow).filter(Workflow.org_id == org_id)
    
    if system_id:
        query = query.filter(Workflow.system_id == system_id)
    
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    
    return PaginatedResponse(
        data={
            "items": [
                WorkflowResponse(
                    id=item.id,
                    org_id=item.org_id,
                    system_id=item.system_id,
                    system_name=item.system.name if item.system else None,
                    name=item.name,
                    description=item.description,
                    yaml_config=item.yaml_config,
                    steps_count=len(item.steps),
                    created_by=item.creator.username if item.creator else None,
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


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["workflow:read"]))
):
    """获取流程详情"""
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="流程不存在")
    
    return WorkflowResponse(
        id=workflow.id,
        org_id=workflow.org_id,
        system_id=workflow.system_id,
        system_name=workflow.system.name if workflow.system else None,
        name=workflow.name,
        description=workflow.description,
        yaml_config=workflow.yaml_config,
        steps_count=len(workflow.steps),
        created_by=workflow.creator.username if workflow.creator else None,
        created_at=workflow.created_at,
        updated_at=workflow.updated_at
    )


@router.post("", response_model=WorkflowResponse, status_code=201)
async def create_workflow(
    request: WorkflowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["workflow:create"]))
):
    """创建流程"""
    workflow = Workflow(
        org_id=request.org_id,
        system_id=request.system_id,
        name=request.name,
        description=request.description,
        yaml_config=request.yaml_config,
        created_by=current_user.id
    )
    db.add(workflow)
    db.commit()
    db.refresh(workflow)
    
    return WorkflowResponse(
        id=workflow.id,
        org_id=workflow.org_id,
        system_id=workflow.system_id,
        name=workflow.name,
        description=workflow.description,
        yaml_config=workflow.yaml_config,
        created_by=current_user.username,
        created_at=workflow.created_at,
        updated_at=workflow.updated_at
    )


@router.put("/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(
    workflow_id: int,
    request: WorkflowUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["workflow:update"]))
):
    """更新流程"""
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="流程不存在")
    
    workflow.name = request.name
    workflow.description = request.description
    workflow.yaml_config = request.yaml_config
    
    db.commit()
    db.refresh(workflow)
    
    return WorkflowResponse(
        id=workflow.id,
        org_id=workflow.org_id,
        system_id=workflow.system_id,
        name=workflow.name,
        description=workflow.description,
        yaml_config=workflow.yaml_config,
        created_by=workflow.creator.username,
        created_at=workflow.created_at,
        updated_at=workflow.updated_at
    )


@router.delete("/{workflow_id}", response_model=ResponseBase)
async def delete_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["workflow:delete"]))
):
    """删除流程"""
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="流程不存在")
    
    db.delete(workflow)
    db.commit()
    
    return ResponseBase()


@router.post("/generate/from-text", response_model=dict)
async def generate_workflow_from_text(
    request: WorkflowGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["workflow:generate"]))
):
    """AI 生成流程 (文字描述)"""
    # TODO: 调用 AI 服务生成流程
    yaml_config = f"""name: AI 生成的流程
nodes:
  - id: node-1
    type: login
    config:
      url: https://example.com
edges:
"""
    
    return {
        "yaml_config": yaml_config,
        "nodes_count": 1,
        "confidence": 0.9,
        "elements_detected": []
    }


@router.post("/{workflow_id}/validate", response_model=WorkflowValidationResponse)
async def validate_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["workflow:validate"]))
):
    """验证流程"""
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="流程不存在")
    
    try:
        config = yaml.safe_load(workflow.yaml_config)
        errors = []
        warnings = []
        
        if "nodes" not in config:
            errors.append("缺少 nodes 配置")
        if "edges" not in config:
            errors.append("缺少 edges 配置")
        
        return WorkflowValidationResponse(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    except yaml.YAMLError as e:
        return WorkflowValidationResponse(
            valid=False,
            errors=[f"YAML 解析错误：{str(e)}"]
        )
