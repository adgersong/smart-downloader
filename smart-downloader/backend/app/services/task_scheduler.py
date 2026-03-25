"""
任务调度器模块
基于 APScheduler 实现定时任务调度
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
from typing import Optional, Dict, Any, Callable
import json
from loguru import logger


class TaskScheduler:
    """任务调度器"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.jobs: Dict[str, Any] = {}
    
    def start(self):
        """启动调度器"""
        self.scheduler.start()
        logger.info("任务调度器已启动")
    
    def shutdown(self, wait: bool = True):
        """关闭调度器"""
        self.scheduler.shutdown(wait=wait)
        logger.info("任务调度器已关闭")
    
    def add_cron_job(
        self,
        job_id: str,
        func: Callable,
        cron_expression: str,
        args: list = None,
        kwargs: dict = None
    ):
        """添加 Cron 定时任务"""
        try:
            # 解析 Cron 表达式
            parts = cron_expression.split()
            if len(parts) == 5:
                minute, hour, day, month, day_of_week = parts
            else:
                raise ValueError("Invalid cron expression")
            
            trigger = CronTrigger(
                minute=minute,
                hour=hour,
                day=day,
                month=month,
                day_of_week=day_of_week
            )
            
            self.scheduler.add_job(
                func=func,
                trigger=trigger,
                id=job_id,
                args=args or [],
                kwargs=kwargs or {},
                replace_existing=True
            )
            
            self.jobs[job_id] = {
                "type": "cron",
                "expression": cron_expression,
                "func": func.__name__,
                "created_at": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Cron 任务已添加：{job_id} ({cron_expression})")
            
        except Exception as e:
            logger.error(f"添加 Cron 任务失败：{job_id} - {str(e)}")
            raise
    
    def add_interval_job(
        self,
        job_id: str,
        func: Callable,
        seconds: int = 0,
        minutes: int = 0,
        hours: int = 0,
        days: int = 0,
        args: list = None,
        kwargs: dict = None
    ):
        """添加间隔任务"""
        try:
            trigger = IntervalTrigger(
                seconds=seconds,
                minutes=minutes,
                hours=hours,
                days=days
            )
            
            self.scheduler.add_job(
                func=func,
                trigger=trigger,
                id=job_id,
                args=args or [],
                kwargs=kwargs or {},
                replace_existing=True
            )
            
            self.jobs[job_id] = {
                "type": "interval",
                "interval": f"{days}d{hours}h{minutes}m{seconds}s",
                "func": func.__name__,
                "created_at": datetime.utcnow().isoformat()
            }
            
            logger.info(f"间隔任务已添加：{job_id}")
            
        except Exception as e:
            logger.error(f"添加间隔任务失败：{job_id} - {str(e)}")
            raise
    
    def add_date_job(
        self,
        job_id: str,
        func: Callable,
        run_date: datetime,
        args: list = None,
        kwargs: dict = None
    ):
        """添加一次性任务"""
        try:
            trigger = DateTrigger(run_date=run_date)
            
            self.scheduler.add_job(
                func=func,
                trigger=trigger,
                id=job_id,
                args=args or [],
                kwargs=kwargs or {},
                replace_existing=True
            )
            
            self.jobs[job_id] = {
                "type": "date",
                "run_date": run_date.isoformat(),
                "func": func.__name__,
                "created_at": datetime.utcnow().isoformat()
            }
            
            logger.info(f"一次性任务已添加：{job_id} ({run_date})")
            
        except Exception as e:
            logger.error(f"添加一次性任务失败：{job_id} - {str(e)}")
            raise
    
    def remove_job(self, job_id: str):
        """移除任务"""
        try:
            self.scheduler.remove_job(job_id)
            if job_id in self.jobs:
                del self.jobs[job_id]
            logger.info(f"任务已移除：{job_id}")
        except Exception as e:
            logger.error(f"移除任务失败：{job_id} - {str(e)}")
    
    def pause_job(self, job_id: str):
        """暂停任务"""
        try:
            self.scheduler.pause_job(job_id)
            logger.info(f"任务已暂停：{job_id}")
        except Exception as e:
            logger.error(f"暂停任务失败：{job_id} - {str(e)}")
    
    def resume_job(self, job_id: str):
        """恢复任务"""
        try:
            self.scheduler.resume_job(job_id)
            logger.info(f"任务已恢复：{job_id}")
        except Exception as e:
            logger.error(f"恢复任务失败：{job_id} - {str(e)}")
    
    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """获取任务信息"""
        return self.jobs.get(job_id)
    
    def get_all_jobs(self) -> Dict[str, Any]:
        """获取所有任务"""
        jobs_info = {}
        for job in self.scheduler.get_jobs():
            jobs_info[job.id] = {
                "id": job.id,
                "name": job.name,
                "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
                "custom_info": self.jobs.get(job.id)
            }
        return jobs_info


# 全局调度器实例
_scheduler = None


def get_scheduler() -> TaskScheduler:
    """获取全局调度器实例"""
    global _scheduler
    if _scheduler is None:
        _scheduler = TaskScheduler()
        _scheduler.start()
    return _scheduler
