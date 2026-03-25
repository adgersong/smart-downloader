#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend')

from app.db.database import engine, Base, get_db
from app.models.user import User
from sqlalchemy.orm import Session
import hashlib

def create_user():
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    
    try:
        # 使用简单哈希
        password_hash = hashlib.sha256("admin123".encode()).hexdigest()
        
        user = User(
            username="admin",
            password_hash=password_hash,
            email="admin@example.com",
            role="admin",
            org_id=1,
            is_active=True
        )
        db.add(user)
        db.commit()
        print(f"✅ 创建用户成功：admin")
        print(f"   组织 ID: 1")
        print(f"   密码：admin123")
    except Exception as e:
        db.rollback()
        print(f"错误：{e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_user()
