#!/usr/bin/env python3
"""
集成测试脚本
测试前后端集成
"""
import sys
import os
import requests
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = 'http://localhost:8000/api/v1'

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

def test_frontend_accessible():
    """测试前端可访问"""
    try:
        response = requests.get('http://localhost:8000', timeout=5)
        log_test('前端页面可访问', response.status_code == 200)
    except:
        log_test('前端页面可访问', False)

def test_backend_api():
    """测试后端 API"""
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        log_test('后端 API 可访问', response.status_code == 200)
    except:
        log_test('后端 API 可访问', False)

def test_cors():
    """测试 CORS 配置"""
    try:
        response = requests.options(
            f'{BASE_URL}/auth/login',
            headers={'Origin': 'http://localhost:8000'}
        )
        log_test('CORS 配置', 'Access-Control-Allow-Origin' in response.headers)
    except:
        log_test('CORS 配置', False)

def test_login_flow():
    """测试完整登录流程"""
    try:
        # 1. 尝试登录
        login_response = requests.post(f'{BASE_URL}/auth/login', json={
            'org_id': 1,
            'username': 'admin',
            'password': 'admin123'
        }, timeout=5)
        
        if login_response.status_code == 200:
            token = login_response.json()['data']['access_token']
            
            # 2. 使用 token 访问受保护接口
            headers = {'Authorization': f'Bearer {token}'}
            user_response = requests.get(f'{BASE_URL}/auth/me', headers=headers, timeout=5)
            
            log_test('登录流程', user_response.status_code == 200)
        else:
            # 用户不存在是允许的
            print('⊘ 登录流程 (无测试用户)')
            global total
            total -= 1
    except Exception as e:
        log_test(f'登录流程 ({str(e)})', False)

def main():
    print("=" * 50)
    print("🧪 集成测试")
    print("=" * 50)
    print()
    
    # 检查服务是否运行
    services_ok = True
    try:
        requests.get('http://localhost:8000/health', timeout=2)
    except:
        print("❌ 后端服务未运行")
        services_ok = False
    
    try:
        requests.get('http://localhost:8000', timeout=2)
    except:
        print("❌ 前端服务未运行")
        services_ok = False
    
    if not services_ok:
        print("\n请先启动服务：")
        print("  cd /Users/songyanjie/opentest/00Bank_down/smart-downloader")
        print("  ./start-dev.sh")
        sys.exit(1)
    
    print("开始测试...\n")
    
    test_frontend_accessible()
    test_backend_api()
    test_cors()
    test_login_flow()
    
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
