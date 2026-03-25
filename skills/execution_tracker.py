#!/usr/bin/env python3
"""
技能执行追踪器
记录每次测试执行情况，生成执行时间表
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

SKILLS_PATH = Path("/Users/songyanjie/opentest/00Bank_down/skills")
EXECUTION_LOG = SKILLS_PATH / "logs" / "execution_history.json"

def log_execution(test_type: str, status: str, details: dict = None):
    """记录执行历史"""
    EXECUTION_LOG.parent.mkdir(parents=True, exist_ok=True)
    
    # 读取现有记录
    if EXECUTION_LOG.exists():
        with open(EXECUTION_LOG, 'r') as f:
            history = json.load(f)
    else:
        history = {"executions": []}
    
    # 添加新记录
    record = {
        "timestamp": datetime.now().isoformat(),
        "test_type": test_type,
        "status": status,
        "details": details or {}
    }
    history["executions"].append(record)
    
    # 只保留最近 1000 条记录
    history["executions"] = history["executions"][-1000:]
    
    # 保存
    with open(EXECUTION_LOG, 'w') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 执行记录已保存：{test_type} - {status}")

def show_history(limit: int = 20):
    """显示执行历史"""
    if not EXECUTION_LOG.exists():
        print("暂无执行记录")
        return
    
    with open(EXECUTION_LOG, 'r') as f:
        history = json.load(f)
    
    executions = history["executions"][-limit:]
    
    print("=" * 70)
    print("技能执行历史")
    print("=" * 70)
    
    for record in reversed(executions):
        status_icon = "✅" if record["status"] == "success" else "❌"
        print(f"{status_icon} {record['timestamp']} - {record['test_type']}")
    
    print("=" * 70)
    print(f"总记录数：{len(history['executions'])}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--history":
        show_history()
    else:
        # 默认记录一次执行
        log_execution("manual_check", "success", {"note": "手动验证"})
        show_history(10)
