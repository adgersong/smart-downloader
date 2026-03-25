#!/usr/bin/env python3
"""
智下载 - 数据库初始化脚本
创建测试组织和用户
"""
import sqlite3
import hashlib
import os

DB_PATH = "backend/data/app.db"

def init_db():
    # 确保数据库目录存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 创建组织表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            config TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 创建用户表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            org_id INTEGER,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
        ''')
        
        # 插入测试组织
        cursor.execute('''
        INSERT OR IGNORE INTO organizations (id, name, config) 
        VALUES (1, '测试组织', '{}')
        ''')
        
        # 插入测试用户 (密码：admin123)
        password_hash = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute('''
        INSERT OR IGNORE INTO users (username, password_hash, email, role, org_id, is_active) 
        VALUES ('admin', ?, 'admin@example.com', 'admin', 1, 1)
        ''', (password_hash,))

        # 插入权限表和 admin 角色权限关联
        permissions = [
            "read_user", "create_user", "update_user", "delete_user",
            "read_organization", "create_organization", "update_organization", "delete_organization",
            "read_workflow", "create_workflow", "update_workflow", "delete_workflow",
            "read_task", "create_task", "update_task", "delete_task",
            "read_file", "upload_file", "delete_file",
            "read_credential", "create_credential", "update_credential", "delete_credential",
            "read_notification", "send_notification"
        ]
        # 创建 permissions 表（如果不存在）
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
        ''')
        # 插入权限记录
        for perm in permissions:
            cursor.execute('INSERT OR IGNORE INTO permissions (name) VALUES (?)', (perm,))
        # 创建 role_permission 关联表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS role_permission (
            role TEXT NOT NULL,
            permission_id INTEGER NOT NULL,
            PRIMARY KEY (role, permission_id),
            FOREIGN KEY (permission_id) REFERENCES permissions(id)
        )
        ''')
        # 为 admin 角色分配所有权限
        cursor.execute('SELECT id FROM permissions')
        perm_ids = [row[0] for row in cursor.fetchall()]
        for pid in perm_ids:
            cursor.execute('INSERT OR IGNORE INTO role_permission (role, permission_id) VALUES (?, ?)', ('admin', pid))
        
        conn.commit()
        
        print("=====================================")
        print("✅ 数据库初始化完成!")
        print("=====================================")
        print("\n登录信息:")
        print("  组织 ID: 1")
        print("  用户名：admin")
        print("  密码：admin123")
        print("\n访问地址:")
        print("  http://localhost:8001/login")
        print("=====================================")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ 错误：{e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
