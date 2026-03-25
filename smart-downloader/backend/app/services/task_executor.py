"""
任务执行服务模块
整合浏览器引擎和工作流引擎执行自动化任务
"""
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import asyncio
import json
from loguru import logger


class TaskExecutor:
    """任务执行器"""
    # (existing content unchanged)
    """任务执行器"""
    
    def __init__(self, workflow_engine, browser_engine):
        self.workflow_engine = workflow_engine
        self.browser_engine = browser_engine
        self.task_status = {}
        self.task_logs = {}
        self.callbacks = {}
    
    def register_callback(self, task_id: int, callback: Callable):
        """注册状态更新回调"""
        self.callbacks[task_id] = callback
    
    async def execute_task(self, task_id: int, org_id: int, workflow_yaml: str) -> Dict[str, Any]:
        """执行任务"""
        logger.info(f"开始执行任务：{task_id}")
        
        self.task_status[task_id] = {
            "status": "running",
            "progress": 0,
            "current_node": None,
            "started_at": datetime.utcnow().isoformat(),
            "completed_at": None,
            "error": None
        }
        
        self.task_logs[task_id] = []
        
        try:
            # 启动浏览器
            await self._log(task_id, "启动浏览器...")
            await self.browser_engine.start(headless=True)
            await self._log(task_id, "浏览器启动成功")
            
            # 构建工作流 - 注入浏览器引擎
            await self._log(task_id, "构建工作流...")
            self.workflow_engine.set_browser_engine(self.browser_engine)
            self.workflow_engine.build_graph(workflow_yaml)
            await self._log(task_id, "工作流构建完成")
            
            # 执行工作流
            await self._log(task_id, "开始执行工作流...")
            
            initial_state = {
                "task_id": task_id,
                "org_id": org_id,
                "current_node": None,
                "completed_nodes": [],
                "failed_nodes": [],
                "node_results": {},
                "status": "running",
                "error_message": None,
                "variables": {}
            }
            
            result = await self.workflow_engine.execute(initial_state)
            
            # 更新状态
            self.task_status[task_id]["status"] = result["status"]
            self.task_status[task_id]["completed_nodes"] = result["completed_nodes"]
            self.task_status[task_id]["progress"] = len(result["completed_nodes"])
            self.task_status[task_id]["completed_at"] = datetime.utcnow().isoformat()
            
            if result["status"] == "failed":
                self.task_status[task_id]["error"] = result["error_message"]
                await self._log(task_id, f"任务执行失败：{result['error_message']}", level="error")
            else:
                await self._log(task_id, "任务执行成功", level="info")
            
            return {
                "task_id": task_id,
                "status": result["status"],
                "completed_nodes": result["completed_nodes"],
                "node_results": result["node_results"]
            }
            
        except Exception as e:
            logger.error(f"任务执行异常：{task_id} - {str(e)}")
            self.task_status[task_id]["status"] = "failed"
            self.task_status[task_id]["error"] = str(e)
            self.task_status[task_id]["completed_at"] = datetime.utcnow().isoformat()
            await self._log(task_id, f"任务执行异常：{str(e)}", level="error")
            
            return {
                "task_id": task_id,
                "status": "failed",
                "error": str(e)
            }
        
        finally:
            # 关闭浏览器
            try:
                await self.browser_engine.close()
                await self._log(task_id, "浏览器已关闭")
            except Exception as e:
                logger.error(f"关闭浏览器失败：{str(e)}")
    
    async def _log(self, task_id: int, message: str, level: str = "info"):
        """记录日志"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message
        }
        
        if task_id not in self.task_logs:
            self.task_logs[task_id] = []
        
        self.task_logs[task_id].append(log_entry)
        
        # 触发回调
        if task_id in self.callbacks:
            await self.callbacks[task_id]({
                "type": "log",
                "task_id": task_id,
                "data": log_entry
            })
    
    def get_task_status(self, task_id: int) -> Optional[Dict[str, Any]]:
        """获取任务状态"""
        return self.task_status.get(task_id)
    
    def get_task_logs(self, task_id: int) -> list:
        """获取任务日志"""
        return self.task_logs.get(task_id, [])
    
    async def stop_task(self, task_id: int):
        """停止任务"""
        if task_id in self.task_status:
            self.task_status[task_id]["status"] = "cancelled"
            self.task_status[task_id]["completed_at"] = datetime.utcnow().isoformat()
            await self._log(task_id, "任务已取消", level="warning")
            
            if task_id in self.callbacks:
                await self.callbacks[task_id]({
                    "type": "status",
                    "task_id": task_id,
                    })

# 全局任务执行器实例（惰性创建）
_executor = None

def get_task_executor() -> TaskExecutor:
    """获取全局任务执行器实例，首次调用时创建并初始化引擎"""
    global _executor
    if _executor is None:
        from ..core.engine.browser_engine import BrowserEngine
        from ..core.engine.workflow_engine import WorkflowEngine
        browser_engine = BrowserEngine()
        workflow_engine = WorkflowEngine()
        _executor = TaskExecutor(workflow_engine=workflow_engine, browser_engine=browser_engine)
    return _executor
