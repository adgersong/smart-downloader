"""
凭证模型
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.database import Base


class Credential(Base):
    """凭证表 (加密存储用户名和密码)"""
    
    __tablename__ = "credentials"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    system_id = Column(Integer, ForeignKey("business_systems.id"), nullable=False, unique=True, index=True)
    username_enc = Column(String(500), nullable=False)  # 加密存储
    password_enc = Column(String(500), nullable=False)  # 加密存储
    auth_type = Column(String(50), nullable=False, default="password")  # password, sms, email
    mfa_config = Column(JSON, nullable=True, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    system = relationship("BusinessSystem", back_populates="credential")
    
    def __repr__(self):
        return f"<Credential(id={self.id}, system_id={self.system_id})>"
