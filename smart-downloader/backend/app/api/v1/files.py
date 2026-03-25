"""
文件管理 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, Form
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
from ...db.database import get_db
from ...models.user import User
from ...schemas import FileListResponse, PaginatedResponse, ResponseBase
from ...core.deps import get_current_user, require_permission
from ..services.file_storage import get_file_storage

router = APIRouter()


@router.get("", response_model=PaginatedResponse)
async def get_files(
    org_id: int = Query(...),
    system_id: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["file:read"]))
):
    """获取文件列表"""
    storage = get_file_storage()
    files = storage.list_files(org_id, system_id, limit=size * page)
    
    total = len(files)
    start = (page - 1) * size
    end = start + size
    
    return PaginatedResponse(
        data={
            "items": files[start:end],
            "pagination": {
                "page": page,
                "size": size,
                "total": total,
                "total_pages": (total + size - 1) // size
            }
        }
    )


@router.get("/stats")
async def get_storage_stats(
    org_id: int = Query(...),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["file:stats"]))
):
    """获取存储统计"""
    storage = get_file_storage()
    return storage.get_storage_stats(org_id)


@router.post("/upload", response_model=dict)
async def upload_file(
    file: UploadFile = File(...),
    org_id: int = Form(...),
    system_id: Optional[int] = Form(None),
    task_id: Optional[int] = Form(None),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission(["file:upload"]))
):
    """上传文件"""
    storage = get_file_storage()
    
    content = await file.read()
    result = storage.save_file(
        org_id=org_id,
        file_content=content,
        filename=file.filename,
        system_id=system_id,
        task_id=task_id
    )
    
    return {
        "file_id": result["file_id"],
        "filename": result["filename"],
        "size": result["size"],
        "created_at": result["created_at"]
    }


@router.get("/{file_id}")
async def download_file(
    file_id: str,
    org_id: int = Query(...),
    current_user: User = Depends(get_current_user)
):
    """下载文件"""
    storage = get_file_storage()
    
    content = storage.get_file(org_id, file_id)
    if not content:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return StreamingResponse(
        iter([content]),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={file_id}"}
    )


@router.delete("/{file_id}", response_model=ResponseBase)
async def delete_file(
    file_id: str,
    org_id: int = Query(...),
    current_user: User = Depends(get_current_user)
):
    """删除文件"""
    storage = get_file_storage()
    
    success = storage.delete_file(org_id, file_id)
    if not success:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return ResponseBase()
