#!/usr/bin/env python3
"""
后端单元测试脚本
测试后端模型和服务
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend'))

from app.models.organization import Organization
from app.models.user import User
from app.models.business_system import BusinessSystem
from app.db.database import SessionLocal, engine

total = 0
passed = 0
failed = 0

def log_test(name, status):
    global total, passed, failed
    total += 1
    if status:
        print(f"✓ {name}")
        passed += 1
    else:
        print(f"✗ {name}")
        failed += 1

def test_db_connection():
    try:
        from sqlalchemy import text
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        log_test("数据库连接", True)
    except Exception as e:
        log_test(f"数据库连接 ({str(e)})", False)

def test_organization_model():
    """测试组织模型"""
    try:
        org = Organization(name="测试组织", config={})
        log_test("组织模型创建", org.name == "测试组织")
    except Exception as e:
        log_test(f"组织模型 ({str(e)})", False)

def test_user_model():
    """测试用户模型"""
    try:
        user = User(username="testuser", password_hash="hash123", role="user", org_id=1)
        log_test("用户模型创建", user.username == "testuser")
    except Exception as e:
        log_test(f"用户模型 ({str(e)})", False)

def test_business_system_model():
    """测试业务系统模型"""
    try:
        system = BusinessSystem(
            name="测试系统",
            url="https://test.com",
            type="custom",
            org_id=1
        )
        log_test("业务系统模型创建", system.name == "测试系统")
    except Exception as e:
        log_test(f"业务系统模型 ({str(e)})", False)

def main():
    print("=" * 50)
    print("🧪 后端单元测试")
    print("=" * 50)
    print()
    
    test_db_connection()
    test_organization_model()
    test_user_model()
    test_business_system_model()
    
    print()
    print("=" * 50)
    print(f"总计：{total}")
    print(f"通过：{passed}")
    print(f"失败：{failed}")
    if total > 0:
        print(f"通过率：{passed * 100 // total}%")
    print("=" * 50)
    
    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
