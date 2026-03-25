#!/usr/bin/env python3
"""
交互测试脚本
模拟真实用户从登录到页面操作的完整流程
"""
import sys
import os
import requests
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = 'http://localhost:8000/api/v1'

class TestResult:
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
    
    def log(self, name, status):
        self.total += 1
        if status:
            print(f"✓ {name}")
            self.passed += 1
        else:
            print(f"✗ {name}")
            self.failed += 1

def test_login_flow(result):
    """测试完整登录流程"""
    print("\n【登录流程测试】")
    
    try:
        # 1. 尝试登录
        print("  1. 提交登录请求...")
        login_response = requests.post(f'{BASE_URL}/auth/login', json={
            'org_id': 1,
            'username': 'admin',
            'password': 'admin123'
        }, timeout=5)
        
        if login_response.status_code == 200:
            token = login_response.json()['data']['access_token']
            result.log("登录成功", True)
            
            # 2. 获取用户信息
            print("  2. 获取用户信息...")
            headers = {'Authorization': f'Bearer {token}'}
            user_response = requests.get(f'{BASE_URL}/auth/me', headers=headers, timeout=5)
            result.log("获取用户信息", user_response.status_code == 200)
            
            return token
        else:
            result.log("登录 (用户不存在)", False)
            print("  ⊘ 跳过后续需要认证的测试")
            return None
    except Exception as e:
        result.log(f"登录流程 ({str(e)})", False)
        return None

def test_organization_crud(result, token):
    """测试组织 CRUD 操作"""
    print("\n【组织管理测试】")
    
    if not token:
        print("  ⊘ 跳过（无认证 token）")
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        # 1. 获取组织列表
        print("  1. 获取组织列表...")
        response = requests.get(f'{BASE_URL}/organizations', headers=headers, timeout=5)
        result.log("获取组织列表", response.status_code == 200)
        
        # 2. 创建组织
        print("  2. 创建组织...")
        create_response = requests.post(f'{BASE_URL}/organizations', headers=headers, json={
            'name': f'测试组织_{int(time.time())}'
        }, timeout=5)
        result.log("创建组织", create_response.status_code == 201)
        
        # 3. 获取组织详情
        if create_response.status_code == 201:
            org_id = create_response.json()['data']['id']
            print(f"  3. 获取组织详情 (ID: {org_id})...")
            detail_response = requests.get(f'{BASE_URL}/organizations/{org_id}', headers=headers, timeout=5)
            result.log("获取组织详情", detail_response.status_code == 200)
            
            # 4. 更新组织
            print("  4. 更新组织...")
            update_response = requests.put(
                f'{BASE_URL}/organizations/{org_id}',
                headers=headers,
                json={'name': '更新后的组织名'},
                timeout=5
            )
            result.log("更新组织", update_response.status_code == 200)
            
            # 5. 删除组织
            print("  5. 删除组织...")
            delete_response = requests.delete(f'{BASE_URL}/organizations/{org_id}', headers=headers, timeout=5)
            result.log("删除组织", delete_response.status_code == 200)
    except Exception as e:
        result.log(f"组织 CRUD ({str(e)})", False)

def test_system_crud(result, token):
    """测试业务系统 CRUD 操作"""
    print("\n【业务系统管理测试】")
    
    if not token:
        print("  ⊘ 跳过（无认证 token）")
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        # 1. 创建业务系统
        print("  1. 创建业务系统...")
        create_response = requests.post(f'{BASE_URL}/systems', headers=headers, json={
            'org_id': 1,
            'name': f'测试系统_{int(time.time())}',
            'url': 'https://test.example.com',
            'type': 'custom'
        }, timeout=5)
        result.log("创建业务系统", create_response.status_code == 201)
        
        # 2. 获取系统列表
        print("  2. 获取系统列表...")
        list_response = requests.get(f'{BASE_URL}/systems?org_id=1', headers=headers, timeout=5)
        result.log("获取系统列表", list_response.status_code == 200)
    except Exception as e:
        result.log(f"业务系统 CRUD ({str(e)})", False)

def main():
    print("=" * 50)
    print("🧪 交互测试 - 完整用户流程")
    print("=" * 50)
    
    # 检查服务是否运行
    try:
        requests.get('http://localhost:8000/health', timeout=2)
    except:
        print("\n❌ 后端服务未运行")
        print("   cd backend && ./start.sh")
        sys.exit(1)
    
    result = TestResult()
    
    # 执行测试
    token = test_login_flow(result)
    test_organization_crud(result, token)
    test_system_crud(result, token)
    
    # 输出结果
    print("\n" + "=" * 50)
    print(f"总计：{result.total}")
    print(f"通过：{result.passed}")
    print(f"失败：{result.failed}")
    if result.total > 0:
        print(f"通过率：{result.passed * 100 // result.total}%")
    print("=" * 50)
    
    return 0 if result.failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
