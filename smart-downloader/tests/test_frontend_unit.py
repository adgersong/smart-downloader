#!/usr/bin/env python3
"""
前端单元测试脚本
使用 Jest 测试前端组件
"""
import subprocess
import sys
import os

def run_frontend_tests():
    """运行前端单元测试"""
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend')
    
    print("=" * 50)
    print("🧪 前端单元测试")
    print("=" * 50)
    
    os.chdir(frontend_dir)
    
    result = subprocess.run(
        ['npm', 'test', '--', '--passWithNoTests', '--watchAll=false'],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    return result.returncode == 0

if __name__ == '__main__':
    success = run_frontend_tests()
    sys.exit(0 if success else 1)
