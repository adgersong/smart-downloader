#!/bin/bash
# 智下载系统 - 测试守护进程停止脚本

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$PROJECT_ROOT/tests/test_daemon.pid"

echo "=========================================="
echo "🛑 停止测试守护进程"
echo "=========================================="
echo ""

if [ -f "$PID_FILE" ]; then
    DAEMON_PID=$(cat "$PID_FILE")
    
    if ps -p "$DAEMON_PID" > /dev/null 2>&1; then
        echo "找到守护进程 (PID: $DAEMON_PID)"
        echo ""
        echo "停止进程..."
        kill "$DAEMON_PID" 2>/dev/null || true
        
        sleep 2
        
        if ps -p "$DAEMON_PID" > /dev/null 2>&1; then
            echo "⚠️  进程未停止，强制终止..."
            kill -9 "$DAEMON_PID" 2>/dev/null || true
        fi
        
        rm -f "$PID_FILE"
        echo ""
        echo "✅ 守护进程已停止"
    else
        echo "⚠️  守护进程未运行 (PID 文件存在但进程不存在)"
        rm -f "$PID_FILE"
    fi
else
    echo "⚠️  未找到守护进程 (PID 文件不存在)"
fi

echo ""
echo "=========================================="
