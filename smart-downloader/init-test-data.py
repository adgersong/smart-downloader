#!/usr/bin/env python3
"""
智下载 - 测试数据初始化脚本
"""
import sys
sys.path.insert(0, 'backend')

from app.db.database import engine, Base, get_db
from app.models.organization import Organization
from app.models.user import User
from app.core.security import get_password_hash
from sqlalchemy.orm import Session

def init_test_data():
    # 创建数据库表
    Base.metadata.create_all(bind=engine)
    
    db = next(get_db())
    
    try:
        # 创建测试组织
        org = Organization(
            name="测试组织",
            config={}
        )
        db.add(org)
        db.commit()
        db.refresh(org)
        print(f"✅ 创建组织：{org.name} (ID: {org.id})")
        
        # 创建测试用户
        user = User(
            username="admin",
            password_hash=get_password_hash("admin123"),
            email="admin@example.com",
            role="admin",
            org_id=org.id,
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"✅ 创建用户：{user.username} (ID: {user.id})")
        
        print("\n=====================================")
        print("测试数据初始化完成!")
        print("=====================================")
        print(f"\n登录信息:")
        print(f"  组织 ID: {org.id}")
        print(f"  用户名：admin")
        print(f"  密码：admin123")
        print("\n访问地址:")
        print(f"  http://localhost:8001/login")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 错误：{e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_test_data()
