#!/usr/bin/env python3
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_path = os.path.join(project_root, 'backend')
sys.path.insert(0, backend_path)

from app.db.database import Base, engine
from app.models import organization, user, business_system, credential, workflow, task

def init_db():
    print("正在初始化数据库...")
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建成功")
    
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"已创建的表：{', '.join(tables)}")
    print(f"总计：{len(tables)} 个表")

if __name__ == "__main__":
    init_db()
