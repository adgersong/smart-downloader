"""
流程和流程步骤模型
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.database import Base


class Workflow(Base):
    """流程表"""
    
    __tablename__ = "workflows"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    system_id = Column(Integer, ForeignKey("business_systems.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    yaml_config = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    organization = relationship("Organization", back_populates="workflows")
    system = relationship("BusinessSystem", back_populates="workflows")
    creator = relationship("User", backref="created_workflows")
    steps = relationship("WorkflowStep", back_populates="workflow", cascade="all, delete-orphan", order_by="WorkflowStep.step_order")
    tasks = relationship("Task", back_populates="workflow", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Workflow(id={self.id}, name='{self.name}')>"


class WorkflowStep(Base):
    """流程步骤表"""
    
    __tablename__ = "workflow_steps"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False, index=True)
    step_order = Column(Integer, nullable=False)
    node_id = Column(String(100), nullable=False)  # 节点唯一标识
    node_type = Column(String(50), nullable=False)  # login, navigate, click, type, wait, download, condition
    config = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关联关系
    workflow = relationship("Workflow", back_populates="steps")
    
    __table_args__ = (
        UniqueConstraint('workflow_id', 'node_id', name='uix_workflow_node'),
    )
    
    def __repr__(self):
        return f"<WorkflowStep(id={self.id}, workflow_id={self.workflow_id}, type='{self.node_type}')>"
