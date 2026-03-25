#!/usr/bin/env python3
"""
测试守护进程
确保持续执行测试，每 5 分钟一次
"""
import subprocess
import time
import os
import sys
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_SCRIPT = os.path.join(PROJECT_ROOT, 'tests', 'run_all_tests.sh')
LOG_FILE = os.path.join(PROJECT_ROOT, 'tests', 'daemon-test.log')
INTERVAL = 300  # 5 分钟

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    with open(LOG_FILE, 'a') as f:
        f.write(log_msg + '\n')

def run_tests():
    log("=" * 60)
    log("开始执行全量测试...")
    log("=" * 60)
    
    try:
        result = subprocess.run(
            ['bash', TEST_SCRIPT],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
        
        log("测试完成")
        log(f"返回码：{result.returncode}")
        
        if result.stdout:
            log("输出:\n" + result.stdout[-2000:])  # 只记录最后 2000 字符
        
        if result.stderr:
            log("错误:\n" + result.stderr[-2000:])
        
        return result.returncode == 0
    except Exception as e:
        log(f"测试执行失败：{str(e)}")
        return False

def main():
    log("测试守护进程启动")
    log(f"测试脚本：{TEST_SCRIPT}")
    log(f"执行间隔：{INTERVAL}秒")
    log(f"日志文件：{LOG_FILE}")
    
    execution_count = 0
    
    while True:
        execution_count += 1
        log(f"\n第 {execution_count} 次执行")
        
        success = run_tests()
        
        if success:
            log("✅ 测试通过")
        else:
            log("❌ 测试失败")
        
        next_run = datetime.now().strftime('%H:%M:%S')
        log(f"\n下次执行时间：{next_run}")
        log(f"等待 {INTERVAL} 秒...\n")
        
        time.sleep(INTERVAL)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        log("\n守护进程已停止")
        sys.exit(0)
