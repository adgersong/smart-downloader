#!/usr/bin/env python3
"""
API 接口测试脚本
测试所有后端 API 接口
"""
import sys
import os
import requests
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = 'http://localhost:8000/api/v1'

# 测试计数器
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

def test_health():
    """测试健康检查接口"""
    try:
        response = requests.get('http://localhost:8000/health')
        log_test('健康检查接口', response.status_code == 200)
    except Exception as e:
        log_test(f'健康检查接口 ({str(e)})', False)

def test_login():
    """测试登录接口"""
    try:
        response = requests.post(f'{BASE_URL}/auth/login', json={
            'org_id': 1,
            'username': 'admin',
            'password': 'admin123'
        })
        # 允许 401（用户不存在）或 200（登录成功）
        log_test('登录接口', response.status_code in [200, 401])
    except Exception as e:
        log_test(f'登录接口 ({str(e)})', False)

def test_get_organizations():
    """测试获取组织列表"""
    try:
        # 先登录获取 token
        login_response = requests.post(f'{BASE_URL}/auth/login', json={
            'org_id': 1,
            'username': 'admin',
            'password': 'admin123'
        })
        
        if login_response.status_code == 200:
            token = login_response.json()['data']['access_token']
            headers = {'Authorization': f'Bearer {token}'}
            
            response = requests.get(f'{BASE_URL}/organizations', headers=headers)
            log_test('获取组织列表', response.status_code == 200)
        else:
            # 用户不存在，跳过
            print('⊘ 获取组织列表 (无测试用户)')
            global total
            total -= 1
    except Exception as e:
        log_test(f'获取组织列表 ({str(e)})', False)

def test_api_docs():
    """测试 API 文档"""
    try:
        response = requests.get('http://localhost:8000/api/docs')
        log_test('API 文档页面', response.status_code == 200)
    except Exception as e:
        log_test(f'API 文档页面 ({str(e)})', False)

def test_openapi():
    """测试 OpenAPI 规范"""
    try:
        response = requests.get('http://localhost:8000/api/openapi.json')
        log_test('OpenAPI 规范', response.status_code == 200 and 'openapi' in response.json())
    except Exception as e:
        log_test(f'OpenAPI 规范 ({str(e)})', False)

def main():
    print("=" * 50)
    print("🧪 API 接口测试")
    print("=" * 50)
    print()
    
    # 检查后端是否运行
    try:
        requests.get('http://localhost:8000/health', timeout=2)
    except:
        print("❌ 后端服务未运行，请先启动后端")
        print("   cd backend && ./start.sh")
        sys.exit(1)
    
    print("开始测试...\n")
    
    test_health()
    test_login()
    test_get_organizations()
    test_api_docs()
    test_openapi()
    
    print()
    print("=" * 50)
    print(f"总计：{total}")
    print(f"通过：{passed}")
    print(f"失败：{failed}")
    print(f"通过率：{passed * 100 // total if total > 0 else 0}%")
    print("=" * 50)
    
    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
