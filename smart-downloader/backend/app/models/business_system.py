"""
业务系统模型
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.database import Base


class BusinessSystem(Base):
    """业务系统表"""
    
    __tablename__ = "business_systems"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False)
    type = Column(String(50), nullable=True)  # erp, financial, crm, custom
    description = Column(Text, nullable=True)
    login_config = Column(JSON, nullable=True, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    organization = relationship("Organization", back_populates="systems")
    credential = relationship("Credential", back_populates="system", uselist=False, cascade="all, delete-orphan")
    workflows = relationship("Workflow", back_populates="system", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<BusinessSystem(id={self.id}, name='{self.name}', type='{self.type}')>"
