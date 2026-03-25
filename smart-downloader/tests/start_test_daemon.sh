#!/bin/bash
# 智下载系统 - 测试守护进程启动脚本

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DAEMON_SCRIPT="$PROJECT_ROOT/tests/test_daemon.py"
PID_FILE="$PROJECT_ROOT/tests/test_daemon.pid"
LOG_FILE="$PROJECT_ROOT/tests/daemon-test.log"

echo "=========================================="
echo "🚀 启动测试守护进程"
echo "=========================================="
echo ""

# 检查是否已在运行
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "⚠️  守护进程已在运行 (PID: $OLD_PID)"
        echo ""
        echo "停止旧进程:"
        echo "  kill $(cat $PID_FILE)"
        echo ""
        read -p "是否继续？(y/N): " confirm
        if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
            exit 0
        fi
        kill "$OLD_PID" 2>/dev/null || true
        sleep 1
    fi
    rm -f "$PID_FILE"
fi

# 启动守护进程
echo "📍 项目目录：$PROJECT_ROOT"
echo "📍 日志文件：$LOG_FILE"
echo "📍 PID 文件：$PID_FILE"
echo "📍 执行间隔：300 秒 (5 分钟)"
echo ""
echo "启动守护进程..."

nohup python3 "$DAEMON_SCRIPT" > "$LOG_FILE" 2>&1 &
DAEMON_PID=$!

echo $DAEMON_PID > "$PID_FILE"

sleep 2

if ps -p "$DAEMON_PID" > /dev/null 2>&1; then
    echo "✅ 守护进程已启动"
    echo ""
    echo "进程信息:"
    echo "  PID: $DAEMON_PID"
    echo "  状态：运行中"
    echo ""
    echo "管理命令:"
    echo "  查看日志：tail -f $LOG_FILE"
    echo "  查看状态：ps -p $DAEMON_PID"
    echo "  停止进程：kill $DAEMON_PID"
    echo "  查看 PID: cat $PID_FILE"
    echo ""
    echo "=========================================="
else
    echo "❌ 守护进程启动失败"
    exit 1
fi
