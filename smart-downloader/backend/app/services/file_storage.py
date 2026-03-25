"""
文件管理服务模块
管理下载文件的存储、检索和删除
"""
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import shutil
import io
import uuid
from loguru import logger


class FileStorageService:
    """文件存储服务"""
    
    def __init__(self, base_path: str = "./data/files"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def _get_org_path(self, org_id: int) -> Path:
        """获取组织文件路径"""
        org_path = self.base_path / str(org_id)
        org_path.mkdir(parents=True, exist_ok=True)
        return org_path
    
    def _get_date_path(self, org_path: Path, date: Optional[str] = None) -> Path:
        """获取日期文件路径"""
        if not date:
            date = datetime.utcnow().strftime("%Y-%m-%d")
        date_path = org_path / date
        date_path.mkdir(parents=True, exist_ok=True)
        return date_path
    
    def save_file(
        self,
        org_id: int,
        file_content: bytes,
        filename: str,
        system_id: Optional[int] = None,
        task_id: Optional[int] = None,
        date: Optional[str] = None
    ) -> Dict[str, Any]:
        """保存文件"""
        # 生成唯一文件名
        file_ext = Path(filename).suffix
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        
        # 获取存储路径
        org_path = self._get_org_path(org_id)
        date_path = self._get_date_path(org_path, date)
        
        # 如果指定了 system_id，创建系统子目录
        if system_id:
            system_path = date_path / f"system_{system_id}"
            system_path.mkdir(parents=True, exist_ok=True)
            save_path = system_path / unique_filename
        else:
            save_path = date_path / unique_filename
        
        # 保存文件
        with open(save_path, "wb") as f:
            f.write(file_content)
        
        logger.info(f"文件已保存：{save_path}")
        
        return {
            "file_id": unique_filename,
            "filename": filename,
            "path": str(save_path),
            "size": len(file_content),
            "org_id": org_id,
            "system_id": system_id,
            "task_id": task_id,
            "created_at": datetime.utcnow().isoformat()
        }
    
    def get_file(
        self,
        org_id: int,
        file_id: str
    ) -> Optional[bytes]:
        """获取文件内容"""
        org_path = self._get_org_path(org_id)
        
        # 搜索文件
        for file_path in org_path.rglob(file_id):
            if file_path.is_file():
                with open(file_path, "rb") as f:
                    return f.read()
        
        return None
    
    def get_file_url(
        self,
        org_id: int,
        file_id: str
    ) -> Optional[str]:
        """获取文件 URL"""
        org_path = self._get_org_path(org_id)
        
        for file_path in org_path.rglob(file_id):
            if file_path.is_file():
                return f"/api/v1/files/{org_id}/{file_id}"
        
        return None
    
    def delete_file(
        self,
        org_id: int,
        file_id: str
    ) -> bool:
        """删除文件"""
        org_path = self._get_org_path(org_id)
        
        for file_path in org_path.rglob(file_id):
            if file_path.is_file():
                file_path.unlink()
                logger.info(f"文件已删除：{file_path}")
                return True
        
        return False
    
    def list_files(
        self,
        org_id: int,
        system_id: Optional[int] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """列出文件"""
        org_path = self._get_org_path(org_id)
        files = []
        
        # 搜索文件
        for file_path in org_path.rglob("*"):
            if not file_path.is_file():
                continue
            
            # 过滤系统 ID
            if system_id:
                if f"system_{system_id}" not in str(file_path):
                    continue
            
            # 过滤日期
            file_date = file_path.parent.name
            if date_from and file_date < date_from:
                continue
            if date_to and file_date > date_to:
                continue
            
            files.append({
                "file_id": file_path.name,
                "filename": file_path.name,
                "path": str(file_path),
                "size": file_path.stat().st_size,
                "created_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                "org_id": org_id
            })
            
            if len(files) >= limit:
                break
        
        return files
    
    def get_storage_stats(self, org_id: int) -> Dict[str, Any]:
        """获取存储统计"""
        org_path = self._get_org_path(org_id)
        
        total_size = 0
        file_count = 0
        
        for file_path in org_path.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
                file_count += 1
        
        return {
            "org_id": org_id,
            "file_count": file_count,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / 1024 / 1024, 2)
        }
    
    def cleanup_old_files(self, org_id: int, days: int = 30) -> int:
        """清理旧文件"""
        org_path = self._get_org_path(org_id)
        cutoff = datetime.utcnow().timestamp() - (days * 24 * 60 * 60)
        deleted_count = 0
        
        for file_path in org_path.rglob("*"):
            if file_path.is_file() and file_path.stat().st_mtime < cutoff:
                file_path.unlink()
                deleted_count += 1
                logger.info(f"已清理旧文件：{file_path.name}")
        
        return deleted_count


# 全局服务实例
_storage = None


def get_file_storage() -> FileStorageService:
    """获取全局文件存储服务实例，根据 SETTINGS 决定本地或 MinIO"""
    global _storage
    if _storage is None:
        from ..core.config.settings import Settings
        settings = Settings()
        if settings.FILE_STORAGE == "minio":
            # 延迟导入 MinIO 客户端，若未安装则回退为本地存储
            try:
                from minio import Minio
                class MinIOFileStorage(FileStorageService):
                    def __init__(self):
                        super().__init__(base_path="")  # base_path unused
                        self.client = Minio(
                            endpoint=settings.MINIO_ENDPOINT.replace("http://", "").replace("https://", ""),
                            access_key=settings.MINIO_ACCESS_KEY,
                            secret_key=settings.MINIO_SECRET_KEY,
                            secure=settings.MINIO_USE_SSL
                        )
                        # 确保 bucket 存在
                        if not self.client.bucket_exists(settings.MINIO_BUCKET):
                            self.client.make_bucket(settings.MINIO_BUCKET)
                    def save_file(self, org_id: int, file_content: bytes, filename: str,
                                   system_id: Optional[int] = None, task_id: Optional[int] = None,
                                   date: Optional[str] = None) -> Dict[str, Any]:
                        # 使用 org_id 作为前缀路径
                        object_name = f"{org_id}/{uuid.uuid4().hex}{Path(filename).suffix}"
                        # 上传到 MinIO，使用 BytesIO 流
                        self.client.put_object(
                            bucket_name=settings.MINIO_BUCKET,
                            object_name=object_name,
                            data=io.BytesIO(file_content),
                            length=len(file_content),
                            content_type="application/octet-stream"
                        )
                        return {
                            "file_id": object_name,
                            "filename": filename,
                            "path": f"minio://{settings.MINIO_BUCKET}/{object_name}",
                            "size": len(file_content),
                            "org_id": org_id,
                            "system_id": system_id,
                            "task_id": task_id,
                            "created_at": datetime.utcnow().isoformat()
                        }
                _storage = MinIOFileStorage()
            except Exception as e:
                # 若 MinIO 客户端不可用，回退本地存储并记录日志
                from loguru import logger
                logger.error(f"MinIO 初始化失败，回退至本地存储: {e}")
                _storage = FileStorageService()
        else:
            # 默认本地文件系统
            _storage = FileStorageService()
    return _storage
