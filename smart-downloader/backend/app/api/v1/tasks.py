"""
任务管理 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from ...db.database import get_db
from ...models.task import Task, TaskExecution
from ...models.workflow import Workflow
from ...models.user import User
from ...schemas import TaskCreate, TaskExecuteRequest, TaskResponse, TaskLogResponse, ResponseBase, PaginatedResponse
from ...services.execution_logger import log_task, LogLevel
from ...core.deps import get_current_user, require_permission

import asyncio
from ...services.task_executor import get_task_executor

router = APIRouter()

# WebSocket 连接管理
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}
    
    async def connect(self, task_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[task_id] = websocket
    
    def disconnect(self, task_id: int):
        if task_id in self.active_connections:
            del self.active_connections[task_id]
    
    async def send_to_task(self, task_id: int, message: dict):
        if task_id in self.active_connections:
            await self.active_connections[task_id].send_json(message)

manager = ConnectionManager()


@router.get("", response_model=PaginatedResponse)
async def get_tasks(
    org_id: int = Query(...),
    workflow_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["task:read"]))
):
    """获取任务列表"""
    query = db.query(Task).filter(Task.org_id == org_id)
    
    if workflow_id:
        query = query.filter(Task.workflow_id == workflow_id)
    if status:
        query = query.filter(Task.status == status)
    
    total = query.count()
    items = query.order_by(Task.created_at.desc()).offset((page - 1) * size).limit(size).all()
    
    return PaginatedResponse(
        data={
            "items": [
                TaskResponse(
                    id=item.id,
                    org_id=item.org_id,
                    workflow_id=item.workflow_id,
                    status=item.status,
                    schedule=item.schedule,
                    context=item.context,
                    created_at=item.created_at,
                    started_at=item.started_at
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


@router.post("/execute", response_model=dict)
async def execute_task(
    request: TaskExecuteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["task:execute"]))
):
    """执行任务"""
    # 创建任务记录
    task = Task(
        org_id=current_user.org_id,
        workflow_id=request.workflow_id,
        status="pending",
        context=request.context or {},
        created_by=current_user.id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    # audit: task creation
    log_task(task.id, f"Task created by user {current_user.id}", LogLevel.INFO)
    
    # 触发实际执行逻辑
    # 获取对应工作流的 yaml 配置
    workflow = db.query(Workflow).filter(Workflow.id == request.workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="工作流不存在")
    # 获取全局执行器实例
    executor = get_task_executor()
    # 注册 WebSocket 回调用于实时推送日志/状态
    async def ws_callback(message: dict):
        await manager.send_to_task(task.id, message)
    executor.register_callback(task.id, ws_callback)
    # 异步启动任务执行（不阻塞 API 返回）
    asyncio.create_task(executor.execute_task(task.id, current_user.org_id, workflow.yaml_config))
    
    return {
        "task_id": task.id,
        "workflow_id": task.workflow_id,
        "status": task.status,
        "estimated_duration": 180,
        "created_at": task.created_at
    }


@router.post("/{task_id}/cancel", response_model=ResponseBase)
async def cancel_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["task:cancel"]))
):
    """取消任务"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    task.status = "cancelled"
    task.completed_at = datetime.utcnow()
    db.commit()
    # audit: task cancellation
    log_task(task.id, f"Task cancelled by user {current_user.id}", LogLevel.INFO)
    
    return ResponseBase(
        data={
            "task_id": task_id,
            "status": "cancelled"
        }
    )


@router.post("/{task_id}/retry", response_model=dict)
async def retry_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["task:retry"]))
):
    """重试任务"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    new_task = Task(
        org_id=task.org_id,
        workflow_id=task.workflow_id,
        status="pending",
        context=task.context,
        created_by=current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    # audit: task retry
    log_task(new_task.id, f"Task retried from {task.id} by user {current_user.id}", LogLevel.INFO)
    
    return {
        "task_id": new_task.id,
        "workflow_id": new_task.workflow_id,
        "status": new_task.status
    }


@router.get("/{task_id}/logs", response_model=TaskLogResponse)
async def get_task_logs(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["task:log"]))
):
    """获取任务执行日志"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    # TODO: 从数据库或文件系统获取日志
    logs = []
    
    return TaskLogResponse(
        task_id=task_id,
        logs=logs
    )


@router.websocket("/ws/{task_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    task_id: int,
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["task:ws"]))
):
    """WebSocket 实时推送任务状态"""
    await manager.connect(task_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(task_id)
