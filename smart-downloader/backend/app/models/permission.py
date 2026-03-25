"""
Permission 模型与 Role‑Permission 关联表
用于基于角色的访问控制（RBAC）
"""

from sqlalchemy import Column, Integer, String, Table, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from ..db.database import Base

# 关联表：角色 <-> 权限（多对多）
role_permission = Table(
    "role_permission",
    Base.metadata,
    Column("role", String(50), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True),
    UniqueConstraint("role", "permission_id", name="uq_role_permission"),
)


class Permission(Base):
    """系统权限定义"""

    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)

    # 通过关联表反向查询拥有此权限的角色（基于 User.role 字段）
    roles = relationship(
        "User",  # 关联 User 表
        secondary=role_permission,
        primaryjoin="Permission.id == role_permission.c.permission_id",
        secondaryjoin="User.role == role_permission.c.role",
        backref="permissions",
        viewonly=True,
    )

    def __repr__(self) -> str:
        return f"<Permission(id={self.id}, name='{self.name}')>"
