"""
任务和任务执行模型
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.database import Base


class Task(Base):
    """任务表"""
    
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False, index=True)
    status = Column(String(50), nullable=False, default="pending")  # pending, running, success, failed, cancelled
    schedule = Column(String(100), nullable=True)  # cron 表达式
    is_active = Column(Boolean, default=True)
    context = Column(JSON, nullable=True, default=dict)  # 运行时变量
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # 关联关系
    organization = relationship("Organization", back_populates="tasks")
    workflow = relationship("Workflow", back_populates="tasks")
    creator = relationship("User", backref="created_tasks")
    executions = relationship("TaskExecution", back_populates="task", cascade="all, delete-orphan", order_by="TaskExecution.created_at.desc()")
    
    def __repr__(self):
        return f"<Task(id={self.id}, workflow_id={self.workflow_id}, status='{self.status}')>"


class TaskExecution(Base):
    """任务执行记录表"""
    
    __tablename__ = "task_executions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False, index=True)
    status = Column(String(50), nullable=False, default="running")  # running, success, failed, cancelled
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    duration = Column(Float, nullable=True)  # 执行时长 (秒)
    result = Column(JSON, nullable=True, default=dict)  # 执行结果
    error_log = Column(Text, nullable=True)  # 错误日志
    screenshots_path = Column(String(500), nullable=True)  # 截图存储路径
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关联关系
    task = relationship("Task", back_populates="executions")
    
    def __repr__(self):
        return f"<TaskExecution(id={self.id}, task_id={self.task_id}, status='{self.status}')>"
