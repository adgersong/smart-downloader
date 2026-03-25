"""
执行日志记录模块
记录任务执行的详细日志
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum
import json
from pathlib import Path
from loguru import logger


class LogLevel(str, Enum):
    """日志级别"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ExecutionLog:
    """执行日志记录器"""
    
    def __init__(self, base_path: Optional[str] = None):
        # 使用配置中的 LOG_DIR，回退到默认路径
        if base_path is None:
            from app.core.config.settings import Settings
            settings = Settings()
            base_path = settings.LOG_DIR
        
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.current_logs: Dict[int, List[Dict]] = {}
    
    def log(
        self,
        task_id: int,
        message: str,
        level: LogLevel = LogLevel.INFO,
        node_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """记录日志"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level.value,
            "task_id": task_id,
            "node_id": node_id,
            "message": message,
            "metadata": metadata or {}
        }
        
        # 添加到内存
        if task_id not in self.current_logs:
            self.current_logs[task_id] = []
        self.current_logs[task_id].append(log_entry)
        
        # 写入文件
        self._write_to_file(task_id, log_entry)
        
        # 使用 loguru 输出
        log_method = getattr(logger, level.value, logger.info)
        log_method(f"[Task {task_id}] {message}")
    
    def _write_to_file(self, task_id: int, log_entry: Dict):
        """写入日志文件"""
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        log_file = self.base_path / f"task_{task_id}_{date_str}.jsonl"
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    
    def get_logs(
        self,
        task_id: int,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        level: Optional[LogLevel] = None,
        limit: int = 100
    ) -> List[Dict]:
        """获取日志"""
        logs = self.current_logs.get(task_id, [])
        
        # 过滤
        if start_time:
            logs = [l for l in logs if l["timestamp"] >= start_time.isoformat()]
        if end_time:
            logs = [l for l in logs if l["timestamp"] <= end_time.isoformat()]
        if level:
            logs = [l for l in logs if l["level"] == level.value]
        
        # 限制数量
        return logs[-limit:]
    
    def get_logs_from_file(
        self,
        task_id: int,
        date: Optional[str] = None
    ) -> List[Dict]:
        """从文件读取日志"""
        if not date:
            date = datetime.utcnow().strftime("%Y-%m-%d")
        
        log_file = self.base_path / f"task_{task_id}_{date}.jsonl"
        
        if not log_file.exists():
            return []
        
        logs = []
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    logs.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        
        return logs
    
    def clear_old_logs(self, days: int = 7):
        """清理旧日志"""
        cutoff = datetime.utcnow().timestamp() - (days * 24 * 60 * 60)
        
        for log_file in self.base_path.glob("task_*.jsonl"):
            if log_file.stat().st_mtime < cutoff:
                log_file.unlink()
                logger.info(f"已删除旧日志文件：{log_file.name}")
    
    def get_task_summary(self, task_id: int) -> Dict[str, Any]:
        """获取任务日志摘要"""
        logs = self.current_logs.get(task_id, [])
        
        if not logs:
            return {
                "total_logs": 0,
                "start_time": None,
                "end_time": None,
                "error_count": 0,
                "warning_count": 0
            }
        
        error_count = sum(1 for l in logs if l["level"] in [LogLevel.ERROR.value, LogLevel.CRITICAL.value])
        warning_count = sum(1 for l in logs if l["level"] == LogLevel.WARNING.value)
        
        return {
            "total_logs": len(logs),
            "start_time": logs[0]["timestamp"] if logs else None,
            "end_time": logs[-1]["timestamp"] if logs else None,
            "error_count": error_count,
            "warning_count": warning_count,
            "last_message": logs[-1]["message"] if logs else None
        }


# 全局日志记录器实例
_logger = None


def get_execution_logger() -> ExecutionLog:
    """获取全局日志记录器实例"""
    global _logger
    if _logger is None:
        _logger = ExecutionLog()
    return _logger


def log_task(task_id: int, message: str, level: LogLevel = LogLevel.INFO):
    """便捷日志函数"""
    get_execution_logger().log(task_id, message, level)
